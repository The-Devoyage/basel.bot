import logging
from datetime import datetime, timezone
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

from classes.user_claims import ShareableLinkClaims
from database.message import MessageModel
import google.generativeai as genai
from classes.socket_message import Button, ButtonAction, SocketMessage
from database.user import UserModel
from database.user_meta import UserMetaModel
from utils.environment import get_env_var

from utils.indexing import (
    create_index,
    get_documents,
    get_agent,
)
from utils.jwt import handle_decode_token, verify_token_session
from utils.subscription import SubscriptionStatus, verify_subscription

router = APIRouter()

logger = logging.getLogger(__name__)

# Constants
GOOGLE_API_KEY = get_env_var("GOOGLE_API_KEY")
SHAREABLE_LINK_SECRET = get_env_var("SHAREABLE_LINK_SECRET")
ALGORITHM = get_env_var("JWT_ALGORITHM")

# Database
message_model = MessageModel("basel.db")
user_model = UserModel("basel.db")
user_meta_model = UserMetaModel("basel.db")

# Gemini Init
genai.configure(api_key=GOOGLE_API_KEY)


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Cookie(None),
    sl_token: Optional[str] = None,
):
    current_user = None
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
            current_user = user_model.get_user_by_uuid(cursor, user_claims.user_uuid)
            if not current_user:
                raise Exception("Current user not found.")
            subscription_status = verify_subscription(
                current_user.id, current_user.created_at
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

        if not chatting_with:
            chatting_with = current_user

        conn.close()

    except Exception as e:
        logger.error(f"{e}")
        return WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

    if not chatting_with:
        raise Exception("No target to represent")

    is_candidate = False
    if current_user is not None and current_user.id == chatting_with.id:
        is_candidate = True

    agent = get_agent(
        is_candidate,
        chatting_with.id,
        current_user,
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
                if current_user and (
                    subscription_status.active or subscription_status.is_free_trial
                ):
                    message_model.create_message(
                        cursor=cursor,
                        text=message.text,
                        sender=message.sender,
                        created_by=current_user.id,
                        updated_by=current_user.id,
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
                if current_user and subscription_status:
                    message_model.create_message(
                        cursor=cursor,
                        text=response.text,
                        sender="bot",
                        created_by=current_user.id,
                        updated_by=current_user.id,
                        user_id=chatting_with.id,
                    )
                    conn.commit()

            except Exception as e:
                logger.error(f"UNEXPECTED ERROR WHILE CONNECTED")
                response = SocketMessage(
                    text="Sorry, I am having some trouble with that. Let's try again.",
                    timestamp=datetime.now(),
                    sender="bot",
                )
                await websocket.send_text(response.model_dump_json())
            finally:
                logger.debug("CLOSING CURSOR")
                cursor.close()
                conn.close()
    except WebSocketDisconnect as e:
        logger.debug(f"WEBSOCKET DISCONNECT: {e}")

        # If the user is the candidate, save the summary
        logger.debug(f"{current_user, subscription_status, chatting_with}")
        try:
            if (
                not current_user
                or current_user.id != chatting_with.id
                or (
                    not subscription_status.active
                    and not subscription_status.is_free_trial
                )
            ):
                conn.close()
                return

            conn = user_meta_model._get_connection()
            cursor = conn.cursor()
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=f"""
                   Summarize the following chat logs by extracting only *new* information that the user has shared today
                        that could help them find or maintain a job. Relevant information includes:
                        - Professional skills or competencies
                        - Day-to-day tasks
                        - Personal hobbies (if relevant to their career)
                        - General knowledge about the user’s career aspirations or goals

                        Rules:
                        - Only include new facts that the user shared today.
                        - Exclude information that the bot brought up or that appears redundant or already known by the bot.
                        - If there are no updates in today’s logs, respond with "None".

                        Format response as JSON:
                            UserMeta = {{'user_meta': str | None}}
                            return UserMeta
                    """,
            )

            logs = message_model.get_messages_by_user_id(
                cursor, current_user.id, chat_start_time
            )

            if not logs:
                return

            logs_story = "\n".join(
                f"{message.sender}: {message.text}" for message in logs
            )

            response = model.generate_content(
                f"Summerize the following chat logs as instructed: {logs_story}",
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                ),
            )

            # Parse the JSON response from the model
            try:
                logger.debug("Updating Index")
                parsed_response = json.loads(
                    response.text
                )  # Assuming response.text contains JSON

                user_meta = parsed_response.get("user_meta")
            except json.JSONDecodeError:
                logger.debug("Failed to decode JSON from response.")
                user_meta = None

            if user_meta and user_meta != "None":
                user_meta_model.create_user_meta(
                    cursor=cursor,
                    user_id=current_user.id,
                    data=user_meta,
                    tags="",  # TODO: Populate tags if available
                    current_user_id=current_user.id,
                )
                conn.commit()

            conn.close()

            # Create Index
            documents = get_documents(current_user.id)
            create_index(documents, current_user.id)
        except Exception as e:
            logger.error(f"FAILED TO SAVE SUMMARY: {e}")
    except Exception as e:
        logger.error(f"UNKNOWN ERROR: {e}")
