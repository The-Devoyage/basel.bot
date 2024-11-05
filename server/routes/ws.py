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
from classes.user_claims import ShareableLinkClaims
from database.message import MessageModel
import google.generativeai as genai
from classes.message import Message
from database.user import UserModel
from database.user_meta import UserMetaModel
from utils.environment import get_env_var

from utils.indexing import (
    get_documents,
    get_agent,
)
from utils.jwt import handle_decode_token, verify_token_session

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

    try:
        conn = user_model._get_connection()
        cursor = conn.cursor()
        if token:
            user_claims = handle_decode_token(token)
            verify_token_session(user_claims.token_session_uuid)
            current_user = user_model.get_user_by_uuid(cursor, user_claims.user_uuid)
            if not current_user:
                raise Exception("Current user not found.")

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
        logger.error(f"FAILED TO AUTHORIZE USER: {e}")
        return WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

    if not chatting_with:
        raise Exception("No target to represent")

    documents = get_documents(chatting_with.id)
    is_candidate = False
    if current_user is not None and current_user.id == chatting_with.id:
        is_candidate = True
    agent = get_agent(documents, is_candidate)

    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()

            conn = message_model._get_connection()
            cursor = conn.cursor()

            try:
                logger.debug(f"USER MESSAGE RECEIVED: {data}")

                message = Message.model_validate_json(data)
                if current_user:
                    message_model.create_message(
                        cursor=cursor,
                        text=message.text,
                        sender=message.sender,
                        created_by=current_user.id,
                        updated_by=current_user.id,
                        user_id=current_user.id,
                    )
                    conn.commit()

                chat_response = agent.chat(message.text)

                logger.debug(f"CHAT RESPONSE: {chat_response}")

                response = Message(
                    text=chat_response.response, timestamp=datetime.now(), sender="bot"
                )
                await websocket.send_text(response.model_dump_json())
                if current_user:
                    message_model.create_message(
                        cursor=cursor,
                        text=response.text,
                        sender="bot",
                        created_by=current_user.id,
                        updated_by=current_user.id,
                        user_id=current_user.id,
                    )
                    conn.commit()

            except Exception as e:
                logger.error(f"UNEXPECTED ERROR WHILE CONNECTED")
                response = Message(
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
        logger.error(f"WEBSOCKET DISCONNECT: {e}")
        try:
            if not current_user:
                conn.close()
                return

            conn = user_meta_model._get_connection()
            cursor = conn.cursor()
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=f"""
                        Summerize the following chat logs by extracting information relevant to the users career that 
                        would help them to find or maintan a job. This can include professional skills, day to day tasks,
                        personal hobbies, and general knowledge about the candidate.

                        Never include skills inferred by the bot, only skills that are explicitly stated by the user.

                        If there are no updates to the chat logs, respond with None.
                    """,
            )

            logs = message_model.get_messages_by_user_id(
                cursor, current_user.id, chat_start_time
            )

            response = model.generate_content(
                f"Summerize the following chat logs as instructed: {logs}"
            )

            if response.text != "None":
                user_meta_model.create_user_meta(
                    cursor=cursor,
                    user_id=current_user.id,
                    data=response.text,
                    tags="",  # TODO: GET TAGS
                    current_user_id=current_user.id,
                )
                conn.commit()

            conn.close()
        except Exception as e:
            logger.error(f"FAILED TO SAVE SUMMARY: {e}")
    except Exception as e:
        logger.error(f"UNKNOWN ERROR: {e}")
