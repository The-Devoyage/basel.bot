import os
import logging
from datetime import datetime
from fastapi import APIRouter, WebSocket
from database.message import MessageModel
import google.generativeai as genai
from classes.message import Message
from database.user import UserModel
from utils.jwt import handle_decode_token

router = APIRouter()

logger = logging.getLogger(__name__)

# Database
message_model = MessageModel("basel.db")
user_model = UserModel("basel.db")

# Initialize the generative model
google_api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=google_api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str):
    await websocket.accept()
    user = None
    if token:
        user_claims = handle_decode_token(token)
        conn = user_model._get_connection()
        cursor = conn.cursor()
        user = user_model.get_user_by_uuid(cursor, user_claims.user_uuid)
        conn.close()
    else:
        raise Exception("Not authorized to access this resource.")

    logger.info(f"User: {user}")

    chat = model.start_chat(
        history=[
            {
                "role": "model",
                "parts": [
                    f"""
                            A new user has connected to this job search platform that you manage called Basel's.
                            You are Basel!

                            Personality:
                            - Friendly
                            - Professional
                            - Hip
                            - Helpful
                            - Inspirational
                            - Generation Alpha (do not lay it on too thick, but be aware of the generation)
                             
                            Help users with the following:
                            - Job search
                            - Job application

                            User Details:
                            - First Name - {user.first_name if user else "Unknown"}
                            - Last Name - {user.last_name if user else "Unknown"}
                            - Email - {user.email if user else "Unknown"}
                            """
                ],
            }
        ]
    )

    while True:
        data = await websocket.receive_text()

        conn = message_model._get_connection()
        cursor = conn.cursor()

        try:
            logger.info(f"Received: {data}")
            message = Message.parse_raw(data)
            message_model.create_message(
                cursor=cursor,
                text=message.text,
                sender=message.sender,
                created_by=1,
                updated_by=1,
                user_id=1,
            )
            conn.commit()

            response = chat.send_message(message.text)

            logger.info(f"Response: {response}")

            if len(response.parts) > 1:
                logger.info(f"Response parts: {len(response.parts)}")

                responses = {}

                if responses:
                    response_parts = [
                        genai.protos.Part(
                            function_response=genai.protos.FunctionResponse(
                                name=fn, response={"result": val}
                            )
                        )
                        for fn, val in responses.items()
                    ]

                    response = chat.send_message(response_parts)

                    if response.text:
                        response = Message(
                            text=response.text, timestamp=datetime.now(), sender="bot"
                        )
                        await websocket.send_text(response.json())
                    else:
                        response = Message(
                            text="Sorry, I don't understand that.. or something went wrong. Please try again.",
                            timestamp=datetime.now(),
                            sender="bot",
                        )
                        await websocket.send_text(response.json())
                else:
                    response = Message(
                        text="Hmm.. I was not able to complete this. Please try again.",
                        timestamp=datetime.now(),
                        sender="bot",
                    )
                    await websocket.send_text(response.json())
            else:
                if not response.text:
                    response = Message(
                        text="Sorry, I don't understand that.. or something went wrong. Please try again.",
                        timestamp=datetime.now(),
                        sender="bot",
                    )
                    await websocket.send_text(response.json())
                else:
                    response = Message(
                        text=response.text, timestamp=datetime.now(), sender="bot"
                    )
                    await websocket.send_text(response.json())
                    message_model.create_message(
                        cursor=cursor,
                        text=response.text,
                        sender="bot",
                        created_by=1,
                        updated_by=1,
                        user_id=1,
                    )
                    conn.commit()
        except Exception as e:
            logger.error(e)
            response = Message(
                text="Sorry, I am having some trouble with that. Let's try again.",
                timestamp=datetime.now(),
                sender="bot",
            )
            await websocket.send_text(response.json())
        finally:
            cursor.close()
            conn.close()
