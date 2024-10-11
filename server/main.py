import os
import logging
import websockets
import asyncio
import google.generativeai as genai
from dotenv import load_dotenv
from pydantic import BaseModel 
from typing import Literal
from datetime import datetime

from database.message import MessageModel
message_model = MessageModel("basel.db")

# Load the environment variables
load_dotenv()

# Configure the logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize the generative model
google_api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=google_api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

class Message(BaseModel):
    text: str
    timestamp: datetime
    sender: Literal["user", "bot"]

# Define a handler for incoming connections
async def chat(websocket):
    chat = model.start_chat()
    response = chat.send_message("""
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
                                 """)
    response = Message(text=response.text, timestamp=datetime.now(), sender="bot")
    await websocket.send(response.json())

    async for raw in websocket:
        conn = message_model._get_connection()
        cursor = conn.cursor()
        try:
            logger.info(f"Received: {raw}")
            message = Message.parse_raw(raw)
            message_model.create_message(cursor=cursor, text=message.text, sender=message.sender, created_by=1, updated_by=1, user_id=1)
            conn.commit()

            response = chat.send_message(message.text)

            logger.info(f"Response: {response}")

            if len(response.parts) > 1:
                logger.info(f"Response parts: {len(response.parts)}")

                responses = {}

                if responses:
                    response_parts = [
                        genai.protos.Part(function_response=genai.protos.FunctionResponse(name=fn, response={"result": val}))
                        for fn, val in responses.items()
                    ]

                    response = chat.send_message(response_parts)

                    if response.text:
                        response = Message(text=response.text, timestamp=datetime.now(), sender="bot")
                        await websocket.send(response.json())
                    else:
                        response = Message(text="Sorry, I don't understand that.. or something went wrong. Please try again.", timestamp=datetime.now(), sender="bot")
                        await websocket.send(response.json())
                else:
                    response = Message(text="Hmm.. I was not able to complete this. Please try again.", timestamp=datetime.now(), sender="bot")
                    await websocket.send(response.json())
            else:
                if not response.text:
                    response = Message(text="Sorry, I don't understand that.. or something went wrong. Please try again.", timestamp=datetime.now(), sender="bot")
                    await websocket.send(response.json())
                else:
                    response = Message(text=response.text, timestamp=datetime.now(), sender="bot")
                    await websocket.send(response.json())
                    message_model.create_message(cursor=cursor, text=response.text, sender="bot", created_by=1, updated_by=1, user_id=1)
                    conn.commit()
        except Exception as e:
            logger.error(e)
            response = Message(text="Sorry, I am having some trouble with that. Let's try again.", timestamp=datetime.now(), sender="bot")
            await websocket.send(response.json())
        finally:
            cursor.close()
            conn.close()

# Start the WebSocket server
async def start_server():
    logger.info("Starting Basels")
    host = os.getenv('HOST')
    port = int(os.getenv('PORT') or 8765)

    server = await websockets.serve(chat, host, port)
    
    # Keep the server running indefinitely
    await server.wait_closed()

# Run the server
asyncio.run(start_server())

