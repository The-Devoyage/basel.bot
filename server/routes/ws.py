import os
import logging
from datetime import datetime
from typing import cast
from fastapi import APIRouter, Cookie, WebSocket, WebSocketException, status
from google.ai.generativelanguage import FunctionResponse, Part
from database.message import MessageModel
import google.generativeai as genai
from classes.message import Message
from database.user import UserModel
from database.user_meta import UserMetaModel
from tools.query_candidate_profile import query_candidate_profile_tool
from tools.create_user_meta import create_user_meta_tool

from utils.indexing import (
    query_candidate_profile,
    get_documents,
    get_query_engine,
)
from utils.jwt import handle_decode_token, verify_token_session

router = APIRouter()

logger = logging.getLogger(__name__)

# Database
message_model = MessageModel("basel.db")
user_model = UserModel("basel.db")
user_meta_model = UserMetaModel("basel.db")

# Initialize Basel
google_api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=google_api_key)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = Cookie(None)):
    user = None
    chat_start_time = datetime.now()

    try:
        if token:
            user_claims = handle_decode_token(token)
            verify_token_session(user_claims.token_session_uuid)
            conn = user_model._get_connection()
            cursor = conn.cursor()
            user = user_model.get_user_by_uuid(cursor, user_claims.user_uuid)
            if not user:
                raise Exception("User not found")
            conn.close()
        else:
            raise Exception("Not authorized to access this resource.")
    except Exception as e:
        logger.error(e)
        return WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

    documents = get_documents(user.id)
    query_engine = get_query_engine(documents)

    await websocket.accept()

    # model = genai.GenerativeModel(
    #     model_name="gemini-1.5-flash",
    #     system_instruction=f"""
    #                         A new user has connected to this job search platform that you manage called Basel's.
    #                         You are a `Basel`, a bot that represents the candidate looking for a job.

    #                         Basel's is a platform that allows candidates to chat with their own personal bot to help them
    #                         with their job search, job application, and career development. The bot learns about the user's
    #                         career, skills, professional experience, professional interest, and professional goals. The candidate
    #                         then can share access to their bot with potential employers to help them learn more about the candidate.

    #                         Personality:
    #                         - Friendly
    #                         - Professional
    #                         - Hip
    #                         - Helpful
    #                         - Inspirational
    #                         - Generation Alpha (do not lay it on too thick, but be aware of the generation)

    #                         When talking with the candidate, help them with their job search, job application, and career development.
    #                         Take the time to learn about the user's career, skills, professional experience, professional interest, and professional goals.
    #                         Additionally, learn about the user's personal interests and hobbies.

    #                         When are talking with the employer, you can help them learn more about the candidate. You can help them
    #                         learn about the user's career, skills, professional experience, professional interest, and professional goals.
    #
    #                         You are talking with:
    #                         - First Name - {user.first_name if user else "Unknown"}
    #                         - Last Name - {user.last_name if user else "Unknown"}
    #                         - Email - {user.email if user else "Unknown"}
    #                         - Role - This user is the candidate. Let's help them with their job search, job application, and career development.
    #
    #                         - Call query_candidate_profile to answer any questions about the candidate.
    #                         - Call create_user_meta to store pertinent information about the candidate whenever the user
    #                         tells you something pertinent about their career or personal life.
    #                         """,
    #     tools=[query_candidate_profile_tool, create_user_meta_tool],
    # )

    # chat = model.start_chat()

    while True:
        data = await websocket.receive_text()

        conn = message_model._get_connection()
        cursor = conn.cursor()

        try:
            logger.debug(f"USER MESSAGE RECEIVED: {data}")

            message = Message.model_validate_json(data)
            message_model.create_message(
                cursor=cursor,
                text=message.text,
                sender=message.sender,
                created_by=user.id,
                updated_by=user.id,
                user_id=user.id,
            )
            conn.commit()

            chat_response = query_engine.chat(message.text)

            logger.debug(f"CHAT RESPONSE: {chat_response}")

            response = Message(
                text=chat_response.response, timestamp=datetime.now(), sender="bot"
            )
            await websocket.send_text(response.model_dump_json())
            message_model.create_message(
                cursor=cursor,
                text=response.text,
                sender="bot",
                created_by=user.id,
                updated_by=user.id,
                user_id=user.id,
            )
            conn.commit()

            # response = chat.send_message(message.text)

            # logger.debug(f"Initial Response: {response}")

            # responses = {}

            # for part in response.parts:
            #     if fn := part.function_call:
            #         logger.info(f"Function Call: {fn}")
            #         if fn.name == "query_candidate_profile":
            #             args = fn.args
            #             responses["query_candidate_profile"] = query_candidate_profile(
            #                 cast(str, args["prompt"]), query_engine
            #             )

            #         if fn.name == "create_user_meta":
            #             args = fn.args
            #             responses[
            #                 "create_user_meta"
            #             ] = user_meta_model.create_user_meta(
            #                 cursor=cursor,
            #                 user_id=user.id,
            #                 data=cast(str, args["data"]),
            #                 tags=cast(str, args["tags"]),
            #                 current_user_id=user.id,
            #             )

            # logger.debug(f"Function Call Responses: {responses}")

            # if responses:
            #     # Handle function call responses
            #     response_parts = [
            #         Part(
            #             function_response=FunctionResponse(
            #                 name=fn, response={"result": val}
            #             )
            #         )
            #         for fn, val in responses.items()
            #     ]

            #     response = chat.send_message(response_parts)

            #     logger.debug(f"Gemini Function Call Response: {response}")

            #     if response.text:
            #         response = Message(
            #             text=response.text, timestamp=datetime.now(), sender="bot"
            #         )
            #         await websocket.send_text(response.model_dump_json())
            #         message_model.create_message(
            #             cursor=cursor,
            #             text=response.text,
            #             sender="bot",
            #             created_by=user.id,
            #             updated_by=user.id,
            #             user_id=user.id,
            #         )
            #         conn.commit()
            #     else:
            #         response = Message(
            #             text="Sorry, I don't understand that.. or something went wrong. Please try again.",
            #             timestamp=datetime.now(),
            #             sender="bot",
            #         )
            #         await websocket.send_text(response.model_dump_json())

            # else:
            #     logger.debug(f"Response: {response}")

            #     response_text = ""

            #     for part in response.parts:
            #         if part.text:
            #             response_text += part.text

            #     response = Message(
            #         text=response_text, timestamp=datetime.now(), sender="bot"
            #     )
            #     await websocket.send_text(response.model_dump_json())
            #     message_model.create_message(
            #         cursor=cursor,
            #         text=response.text,
            #         sender="bot",
            #         created_by=user.id,
            #         updated_by=user.id,
            #         user_id=user.id,
            #     )
            #     conn.commit()

        except Exception as e:
            logger.error(e)
            response = Message(
                text="Sorry, I am having some trouble with that. Let's try again.",
                timestamp=datetime.now(),
                sender="bot",
            )
            await websocket.send_text(response.model_dump_json())
        finally:
            logger.debug("Closing cursor and connection.")
            logger.debug("Summarizing chat logs...")

            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=f"""
                        Summerize the following chat logs by extracting information relevant to the users career that 
                        would help them to find or maintan a job. This can include professional skills, day to day tasks,
                        personal hobbies, and general knowledge about the candidate.

                        Never include skills inferred by the bot, only skills that are explicitly stated by the user.

                        If there are no updates to the chat logs, please respond with "None".
                    """,
            )

            logs = message_model.get_messages_by_user_id(
                cursor, user.id, chat_start_time
            )

            response = model.generate_content(
                f"Summerize the following chat logs as instructed: {logs}"
            )

            logger.debug(f"SUMMARY: {response.text}")

            if response.text != "None":
                user_meta_model.create_user_meta(
                    cursor=cursor,
                    user_id=user.id,
                    data=response.text,
                    tags="",  # TODO: GET TAGS
                    current_user_id=user.id,
                )
                conn.commit()

            cursor.close()
            conn.close()
