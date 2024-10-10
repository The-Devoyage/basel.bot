# Description: A simple web scoket server. Creates a connection to google gemini.
# This is a chat marketplace. Users can chat with the AI to post products and services.
# They can buy and sell products and services.

import os
import logging
import websockets
import asyncio
import google.generativeai as genai
from dotenv import load_dotenv
from controllers.product import create_product, get_products
from pydantic import BaseModel 
from typing import Literal, Optional, List
from datetime import datetime

from controllers.match import match_function_call

# Load the environment variables
load_dotenv()

# Configure the logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize the generative model
google_api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=google_api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-flash", tools=[get_products, create_product])

class Product(BaseModel):
    product_id: int
    name: str
    description: str
    url: str
    thumbnail_url: str
    status: bool

class Message(BaseModel):
    text: str
    timestamp: datetime
    sender: Literal["user", "bot"]
    products: Optional[List[Product]]

# Define a handler for incoming connections
async def chat(websocket):
    chat = model.start_chat()
    response = chat.send_message("""
                                 A new user has connected to the AI Marketplace that you manage called Basel's.

                                 You are Basel!

                                 Personality:
                                 - Friendly
                                 - Professional
                                 - Hip
                                 - Helpful
                                 - Inspirational
                                 - Generation Alpha (do not lay it on too thick, but be aware of the generation)

                                 Help users with the following:

                                 Creating or Adding Products to the Database:
                                 - Users can ask you to create a product for them. You can ask them for the URL. 
                                 - To create a product, call the create_product tool. 
                                 - The only requirement to add a product is the URL. 

                                 Searching or Finding products: 
                                 - Your primary job is to search for products and return them to the user.
                                 - When a user asks you to find a product, then you should generate and use keywords to 
                                 search for products in the database using the get_products function. 
                                 - When choosing keywords, consider variations of the words, synonyms, and related words. 
                                 - Always use at least 10 keywords. 
                                 - When dealing with results of products in groups, only give a short summerization of the group. 
                                 - You don't need to describe each product in detail because the API returns the detailed description 
                                 outside the context of your conversation.

                                 Rules:
                                 - If the user tries to do anything other than create or find products, you can respond with
                                 a friendly message that you are here to help them with products and services.

                                 Initial Instruction:
                                 - Greet the user.
                                 - Start by asking them what product they would like to find.
                                 - They might respond with a product description or search query, if they do, simply search for products.
                                 """)
    response = Message(text=response.text, timestamp=datetime.now(), sender="bot", products=[])
    await websocket.send(response.json())

    async for raw in websocket:
        try:
            logger.info(f"Received: {raw}")
            message = Message.parse_raw(raw)

            response = chat.send_message(message.text)

            logger.info(f"Response: {response}")

            if len(response.parts) > 1:
                logger.info(f"Response parts: {len(response.parts)}")

                responses = {}

                for part in response.parts:
                    if fn := part.function_call:
                        result = match_function_call(fn)
                        if result:
                            responses[fn.name] = result

                logger.info(f"Responses: {responses}")


                if responses:
                    response_parts = [
                        genai.protos.Part(function_response=genai.protos.FunctionResponse(name=fn, response={"result": val}))
                        for fn, val in responses.items()
                    ]

                    response = chat.send_message(response_parts)

                    if response.text:
                        response = Message(text=response.text, timestamp=datetime.now(), sender="bot", products=responses.get("get_products", []))
                        await websocket.send(response.json())
                    else:
                        response = Message(text="Sorry, I don't understand that.. or something went wrong. Please try again.", timestamp=datetime.now(), sender="bot", products=[])
                        await websocket.send(response.json())
                else:
                    response = Message(text="Hmm.. I was not able to complete this. Please try again.", timestamp=datetime.now(), sender="bot", products=[])
                    await websocket.send(response.json())
            else:
                if not response.text:
                    response = Message(text="Sorry, I don't understand that.. or something went wrong. Please try again.", timestamp=datetime.now(), sender="bot", products=[])
                    await websocket.send(response.json())
                else:
                    response = Message(text=response.text, timestamp=datetime.now(), sender="bot", products=[])
                    await websocket.send(response.json())
        except Exception as e:
            logger.error(e)
            response = Message(text="Sorry, I am having some trouble with that. Let's try again.", timestamp=datetime.now(), sender="bot", products=[])
            await websocket.send(response.json())

# Start the WebSocket server
async def start_server():
    logger.info("Starting the application.")
    host = os.getenv('HOST')
    port = int(os.getenv('PORT') or 8765)

    server = await websockets.serve(chat, host, port)
    
    # Keep the server running indefinitely
    await server.wait_closed()

# Run the server
asyncio.run(start_server())

