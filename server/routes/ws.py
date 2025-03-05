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
from llama_index.core.agent.workflow import (
    AgentOutput,
    AgentStream,
    ToolCall,
    ToolCallResult,
)
from basel.agent import get_agent
from basel.indexing import add_index, get_documents, create_s3_documents

from classes.user_claims import ShareableLinkClaims
from classes.socket_message import MessageType, SocketMessage
from database.interview_assessment import InterviewAssessment
from database.organization_user import OrganizationUser
from database.shareable_link import ShareableLink
from database.message import Message, SenderIdentifer
from database.user import User
from utils.environment import get_env_var
from utils.brokers import ws_broker, ui_events

from utils.jwt import handle_decode_token, verify_token_session
from utils.subscription import SubscriptionStatus

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
    interview_assessment_uuid: Optional[UUID] = None,
):
    user_claims = None
    chatting_with = None
    chat_start_time = datetime.now(timezone.utc)
    subscription_status = SubscriptionStatus(
        active=False, subscription=None, is_free_trial=False
    )
    shareable_link = None
    interview_assessment = None
    message_count = 0

    logger.debug(f"INTERVIEW ASSESSMENT UUID {interview_assessment_uuid}")
    try:
        if token:
            user_claims = await handle_decode_token(token)
            await verify_token_session(user_claims.token_session_uuid)
            subscription_status = user_claims.subscription_status

        if sl_token:
            decoded = jwt.decode(
                sl_token, SHAREABLE_LINK_SECRET, algorithms=[ALGORITHM]
            )
            sl_claims = cast(ShareableLinkClaims, ShareableLinkClaims(**decoded))
            shareable_link = await ShareableLink.find_one(
                ShareableLink.uuid == UUID(sl_claims.shareable_link_uuid)
            )
            chatting_with = await User.find_one(User.uuid == UUID(sl_claims.user_uuid))
            if not chatting_with:
                logger.debug("SHAREABLE LINK TOKEN USER NOT FOUND")
                raise Exception("Shareable Link Token User Not Found")

        if interview_assessment_uuid and user_claims:
            logger.debug("FINDING ASSESSMENT USER")
            interview_assessment = await InterviewAssessment.find_one(
                InterviewAssessment.uuid == interview_assessment_uuid, fetch_links=True
            )
            if not interview_assessment:
                logger.debug("INTERVIEW ASSESSMENT NOT FOUND")
                raise Exception("Interview Assessment Not Found")

            organization_user = await OrganizationUser.find_one(
                OrganizationUser.user.id == user_claims.user.id,  # type:ignore
                OrganizationUser.organization.id  # type:ignore
                == interview_assessment.interview.organization.id,  # type:ignore
                fetch_links=True,
            )
            if not organization_user:
                logger.debug("ORGANIZATION USER NOT FOUND")
                raise Exception("Organization User Not Found. Access denied.")
            chatting_with = interview_assessment.user

        if user_claims and (not sl_token and not interview_assessment):
            logger.debug("DEFAULTING TO CURRENT USER")
            chatting_with = user_claims.user

        logger.debug(f"CHATTING WITH {chatting_with}")

    except Exception as e:
        logger.debug(f"{e}")
        return WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

    if (
        user_claims is not None
        and chatting_with is not None
        and user_claims.user.id == chatting_with.id  # type:ignore
    ):
        is_candidate = True
    else:
        is_candidate = False

    await websocket.accept()

    if user_claims and user_claims.user and user_claims.user.uuid:
        ws_broker[user_claims.user.uuid] = websocket

    handler = await get_agent(
        is_candidate,
        chatting_with,  # type:ignore
        user_claims,
        subscription_status,
        shareable_link,
    )

    try:
        while True:
            data = await websocket.receive_text()

            try:
                logger.debug(f"USER MESSAGE RECEIVED: {data}")

                incoming = SocketMessage.model_validate_json(data)

                # Handle Index Files Attached to Message
                if incoming.files and user_claims:
                    create_s3_documents(user=user_claims.user, files=incoming.files)

                logger.debug(
                    f"CRED CHECK: {user_claims} - {subscription_status} - {chatting_with}"
                )

                # Handle save message
                if (
                    user_claims
                    and (
                        subscription_status.active or subscription_status.is_free_trial
                    )
                    and chatting_with
                ):
                    await Message(
                        user=chatting_with,  # type:ignore
                        sender=incoming.sender,
                        text=incoming.text,
                        created_by=user_claims.user,  # type:ignore
                        context=incoming.context,
                    ).create()

                # Handle create response
                prompt = incoming.text
                if incoming.files:
                    prompt += f"\n\n #Attached Files: {incoming.files}"
                if incoming.context:
                    prompt += f"\n\n #Context: {incoming.context}"

                # chat_response = await agent.astream_chat(prompt)
                handler.run(user_msg=prompt)

                current_agent = None
                response_text = ""
                chat_time = datetime.now()

                async for event in handler.stream_events():
                    if (
                        hasattr(event, "current_agent_name")
                        and event.current_agent_name != current_agent
                    ):
                        current_agent = event.current_agent_name
                        print(f"\n{'='*50}")
                        print(f"🤖 Agent: {current_agent}")
                        print(f"{'='*50}\n")

                    if isinstance(event, AgentStream):
                        if event.delta:
                            print(f"\n{'='*50}")
                            print(f"⭐ Agent Stream")
                            print(f"{'='*50}\n")
                            print(event.delta, end="", flush=True)
                            response = SocketMessage(
                                text=event.delta,
                                message_type=MessageType.MESSAGE,
                                timestamp=chat_time,
                                sender=SenderIdentifer.BOT,
                                buttons=None,
                            )
                            # Respond to user
                            await websocket.send_text(response.model_dump_json())
                            response_text += event.delta
                    elif isinstance(event, AgentOutput):
                        if event.tool_calls:
                            print(
                                "🛠️  Planning to use tools:",
                                [call.tool_name for call in event.tool_calls],
                            )
                    elif isinstance(event, ToolCallResult):
                        print(f"🔧 Tool Result ({event.tool_name}):")
                        print(f"  Arguments: {event.tool_kwargs}")
                        print(f"  Output: {event.tool_output}")
                    elif isinstance(event, ToolCall):
                        print(f"🔨 Calling Tool: {event.tool_name}")
                        print(f"  With arguments: {event.tool_kwargs}")

                logger.debug(f"CHAT RESPONSE {response_text}")

                end_response = SocketMessage(
                    text=response_text,
                    message_type=MessageType.END,
                    timestamp=chat_time,
                    sender=SenderIdentifer.BOT,
                    buttons=None,
                )
                await websocket.send_text(end_response.model_dump_json())

                # Send UI Events
                if (
                    user_claims
                    and user_claims.user
                    and user_claims.user.uuid in ui_events
                ):
                    for event in ui_events[user_claims.user.uuid]:
                        await websocket.send_text(event)
                    ui_events[user_claims.user.uuid] = []

                # Track SL Views
                if message_count == 0 and shareable_link:
                    shareable_link.views = shareable_link.views + 1
                    await shareable_link.save()

                message_count += 1
                if user_claims and subscription_status and chatting_with:
                    await Message(
                        user=chatting_with,  # type:ignore
                        sender=SenderIdentifer.BOT,
                        text=response_text,
                        created_by=user_claims.user,  # type:ignore
                    ).create()

            except Exception as e:
                logger.debug(f"UNEXPECTED ERROR WHILE CONNECTED: {e}")
                socket_response = SocketMessage(
                    text="Sorry, I am having some trouble with that. Let's try again.",
                    timestamp=datetime.now(),
                    sender=SenderIdentifer.BOT,
                )
                await websocket.send_text(socket_response.model_dump_json())
    except WebSocketDisconnect as e:
        logger.debug(f"WEBSOCKET DISCONNECT: {e}")

        try:
            logger.debug("SYNC NEW USER META")
            if (
                not user_claims
                or not chatting_with
                or user_claims.user.id != chatting_with.id  # type:ignore
                or (
                    not subscription_status.active
                    and not subscription_status.is_free_trial
                )
            ):
                logger.debug("CLOSING WITHOUT SYNCING NEW USER META")
                return
            documents = get_documents(user_claims.user, chat_start_time)
            add_index(documents, "user_meta")

        except Exception as e:
            logger.debug(e)

    except Exception as e:
        logger.debug(f"UNKNOWN ERROR: {e}")
