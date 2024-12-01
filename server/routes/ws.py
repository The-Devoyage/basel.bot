import logging
from datetime import datetime, timezone
from time import time
from typing import Optional, cast
from fastapi import (
    APIRouter,
    Cookie,
    WebSocket,
    WebSocketDisconnect,
    WebSocketException,
    status,
)
import jwt
import json
from llama_index.llms.openai import OpenAI
from pydantic import BaseModel, Field
from basel.agent import get_agent

from classes.user_claims import ShareableLinkClaims
from database.message import MessageModel
from classes.socket_message import Button, ButtonAction, SocketMessage
from database.user import UserModel
from database.user_meta import UserMetaModel
from utils.environment import get_env_var

from basel.indexing import (
    add_to_index,
    get_documents,
)
from utils.jwt import handle_decode_token, verify_token_session
from utils.subscription import SubscriptionStatus, verify_subscription

router = APIRouter()

logger = logging.getLogger(__name__)

# Constants
SHAREABLE_LINK_SECRET = get_env_var("SHAREABLE_LINK_SECRET")
ALGORITHM = get_env_var("JWT_ALGORITHM")

# Database
message_model = MessageModel("basel.db")
user_model = UserModel("basel.db")
user_meta_model = UserMetaModel("basel.db")


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

    try:
        conn = user_model._get_connection()
        cursor = conn.cursor()
        if token:
            user_claims = handle_decode_token(token)
            verify_token_session(user_claims.token_session_uuid)
            subscription_status = verify_subscription(
                user_claims.user.id, user_claims.user.created_at
            )

        if sl_token:
            decoded = jwt.decode(
                sl_token, SHAREABLE_LINK_SECRET, algorithms=[ALGORITHM]
            )
            sl_claims = cast(ShareableLinkClaims, ShareableLinkClaims(**decoded))
            chatting_with = user_model.get_user_by_uuid(cursor, sl_claims.user_uuid)
            if not chatting_with:
                logger.error("SHAREABLE LINK TOKEN USER NOT FOUND")
                raise Exception("Shareable Link Token User Not Found")
        if user_claims and not sl_token:
            chatting_with = user_claims.user

        conn.close()

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

    agent = get_agent(
        is_candidate,
        chatting_with,
        user_claims,
        subscription_status,
    )

    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()

            conn = message_model._get_connection()
            cursor = conn.cursor()

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
                    message_model.create_message(
                        cursor=cursor,
                        text=message.text,
                        sender=message.sender,
                        created_by=user_claims.user.id,
                        updated_by=user_claims.user.id,
                        user_id=chatting_with.id,
                    )
                    conn.commit()

                chat_response = agent.chat(message.text)

                logger.debug(f"CHAT RESPONSE: {chat_response}")

                response = SocketMessage(
                    text=chat_response.response,
                    timestamp=datetime.now(),
                    sender="bot",
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
                await websocket.send_text(response.model_dump_json())
                if user_claims and subscription_status and chatting_with:
                    message_model.create_message(
                        cursor=cursor,
                        text=response.text,
                        sender="bot",
                        created_by=user_claims.user.id,
                        updated_by=user_claims.user.id,
                        user_id=chatting_with.id,
                    )
                    conn.commit()

            except Exception as e:
                logger.error(f"UNEXPECTED ERROR WHILE CONNECTED: {e}")
                socket_response = SocketMessage(
                    text="Sorry, I am having some trouble with that. Let's try again.",
                    timestamp=datetime.now(),
                    sender="bot",
                )
                await websocket.send_text(socket_response.model_dump_json())
            finally:
                logger.debug("CLOSING CURSOR")
                cursor.close()
                conn.close()
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
                conn.close()
                return

            conn = user_meta_model._get_connection()
            cursor = conn.cursor()

            logs = message_model.get_messages(
                cursor, user_claims.user.id, chat_start_time
            )

            if not logs:
                return

            logs_story = "\n".join(
                f"{message.sender}: {message.text}" for message in logs
            )

            class MetaSummary(BaseModel):
                user_meta: str = Field(
                    description="""
                        Summary of chat logs by extracting only *new* information that the user has shared today which
                        could help them find or maintain a job. Relevant information includes:
                        - Professional skills or competencies
                        - Day-to-day tasks
                        - Personal hobbies (if relevant to their career)
                        - General knowledge about the user’s career aspirations or goals

                        Rules:
                        - Only include new facts that the user shared today.
                        - Exclude information that the bot brought up or that appears redundant or already known by the bot.
                        - If there are no updates in today’s logs, respond with "None". Do not use punctuation if responding with the word None.
                                       """
                )

            llm = OpenAI(model="gpt-4o")
            sllm = llm.as_structured_llm(MetaSummary)
            socket_response = sllm.complete(logs_story)

            json_response = json.loads(socket_response.text)
            print(json.dumps(json_response, indent=2))

            if (
                socket_response
                and socket_response is not None
                and socket_response != "None"
            ):
                user_meta_model.create_user_meta(
                    cursor=cursor,
                    user_id=user_claims.user.id,
                    data=json_response["user_meta"],
                    tags="",  # TODO: Populate tags if available
                    current_user_id=user_claims.user.id,
                )
                conn.commit()

            conn.close()

            # Create Index
            documents = get_documents(user_claims.user.id, chat_start_time)
            add_to_index(documents)
        except Exception as e:
            logger.error(f"FAILED TO SAVE SUMMARY: {e}")
    except Exception as e:
        logger.error(f"UNKNOWN ERROR: {e}")
