import logging
from datetime import datetime, timezone
from typing import Optional, cast
from uuid import UUID
from fastapi import (
    APIRouter,
    Cookie,
    WebSocket,
    WebSocketDisconnect,
    WebSocketException,
    status,
)
import jwt
from basel.agent import get_agent
from basel.indexing import add_index, get_documents

from classes.user_claims import ShareableLinkClaims
from classes.socket_message import Button, ButtonAction, SocketMessage
from database.shareable_link import ShareableLink
from database.message import Message, SenderIdentifer
from database.user import User
from utils.environment import get_env_var

from utils.jwt import handle_decode_token, verify_token_session
from utils.subscription import SubscriptionStatus, verify_subscription
from utils.summary import create_summary

router = APIRouter()

logger = logging.getLogger(__name__)

# Constants
SHAREABLE_LINK_SECRET = get_env_var("SHAREABLE_LINK_SECRET")
ALGORITHM = get_env_var("JWT_ALGORITHM")


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Cookie(None),
    sl_token: Optional[str] = None,
):
    user_claims = None
    chatting_with = None
    chat_start_time = datetime.now(timezone.utc)
    subscription_status = SubscriptionStatus(
        active=False, subscriptions=None, is_free_trial=False
    )
    shareable_link = None
    message_count = 0

    try:
        if token:
            user_claims = await handle_decode_token(token)
            await verify_token_session(user_claims.token_session_uuid)
            subscription_status = await verify_subscription(
                user_claims.user, user_claims.user.created_at
            )

        if sl_token:
            decoded = jwt.decode(
                sl_token, SHAREABLE_LINK_SECRET, algorithms=[ALGORITHM]
            )
            sl_claims = cast(ShareableLinkClaims, ShareableLinkClaims(**decoded))
            shareable_link = await ShareableLink.find_one(
                ShareableLink.uuid == UUID(sl_claims.shareable_link_uuid)
            )
            logger.debug(f"SHAREABLE LINK 1: {shareable_link}")
            chatting_with = await User.find_one(User.uuid == UUID(sl_claims.user_uuid))
            if not chatting_with:
                logger.error("SHAREABLE LINK TOKEN USER NOT FOUND")
                raise Exception("Shareable Link Token User Not Found")
        if user_claims and not sl_token:
            chatting_with = user_claims.user

    except Exception as e:
        logger.error(f"{e}")
        return WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

    if (
        user_claims is not None
        and chatting_with is not None
        and user_claims.user.id == chatting_with.id
    ):
        is_candidate = True
    else:
        is_candidate = False

    agent = await get_agent(
        is_candidate,
        chatting_with,
        user_claims,
        subscription_status,
        shareable_link,
    )

    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()

            try:
                logger.debug(f"USER MESSAGE RECEIVED: {data}")

                message = SocketMessage.model_validate_json(data)
                if (
                    user_claims
                    and (
                        subscription_status.active or subscription_status.is_free_trial
                    )
                    and chatting_with
                ):
                    await Message(
                        user=chatting_with,  # type:ignore
                        sender=message.sender,
                        text=message.text,
                        created_by=chatting_with,  # type:ignore
                    ).create()

                chat_response = await agent.achat(message.text)

                logger.debug(f"CHAT RESPONSE: {chat_response}")

                response = SocketMessage(
                    text=chat_response.response,
                    timestamp=datetime.now(),
                    sender=SenderIdentifer.BOT,
                    buttons=[
                        Button(
                            label="Subscribe - $3.99/mo",
                            action=ButtonAction(
                                type="call", endpoint="/subscribe-start"
                            ),
                        )
                    ]
                    if not subscription_status.active
                    or subscription_status.is_free_trial
                    else None,
                )
                # Respond to user
                await websocket.send_text(response.model_dump_json())

                # Track SL Views
                if message_count == 0 and shareable_link:
                    shareable_link.views = shareable_link.views + 1
                    await shareable_link.save()

                message_count += 1
                if user_claims and subscription_status and chatting_with:
                    await Message(
                        user=chatting_with,  # type:ignore
                        sender=SenderIdentifer.BOT,
                        text=response.text,
                        created_by=chatting_with,  # type:ignore
                    ).create()

            except Exception as e:
                logger.error(f"UNEXPECTED ERROR WHILE CONNECTED: {e}")
                socket_response = SocketMessage(
                    text="Sorry, I am having some trouble with that. Let's try again.",
                    timestamp=datetime.now(),
                    sender=SenderIdentifer.BOT,
                )
                await websocket.send_text(socket_response.model_dump_json())
    except WebSocketDisconnect as e:
        logger.debug(f"WEBSOCKET DISCONNECT: {e}")

        try:
            if (
                not user_claims
                or not chatting_with
                or user_claims.user.id != chatting_with.id
                or (
                    not subscription_status.active
                    and not subscription_status.is_free_trial
                )
            ):
                logger.debug("CLOSING WITHOUT SUMMERIZING")
                return
            documents = await get_documents(user_claims.user, chat_start_time)
            add_index(documents, "user_meta")

        except Exception as e:
            logger.error(e)

    except Exception as e:
        logger.error(f"UNKNOWN ERROR: {e}")
