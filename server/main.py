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
from typing import Literal
from datetime import datetime

# Load the environment variables
load_dotenv()

# Configure the logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize the generative model
google_api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=google_api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-flash", tools=[get_products, create_product])

class Message(BaseModel):
    text: str
    timestamp: datetime
    sender: Literal["user", "bot"]

class Product(BaseModel):
    name: str
    description: str
    url: str
    thumbnail_url: str
    status: bool

# Define a handler for incoming connections
async def chat(websocket):
    chat = model.start_chat(enable_automatic_function_calling=True)
    response = chat.send_message("""
                                 A new user has connected to the AI Marketplace that you manage called Basel's.
                                 You are Basel!
                                 Allow the user to browse, create, and buy products and services that
                                 other users have posted. You can also help the user with any questions
                                 about the products and services. Users have the role of both the browser
                                 and the affiliate that posts the links.

                                 Personality:
                                 - Friendly
                                 - Professional
                                 - Hip
                                 - Helpful
                                 - Inspirational
                                 - Generation Alpha (do not lay it on too thick, but be aware of the generation)

                                 You can help users to find products or post products.

                                 - Create products: Users can ask you to create a product for them. You can ask them
                                    for the URL. To create a product, call the create_product tool. You only need the url
                                    to do so, nothing more. Creating a product is the same as "Adding" or "Posting" a product.
                                 - Find products: By default, you help users find products. If they are not adding or creating products,
                                 you should generate and use keywords to search for products in the database using the get_products function. 
                                 When choosing keywords, consider variations of the words, synonyms, and related words. Always use at least 10 keywords.
                                 Always return a description, image, and a link to the product. You can also return the price and other details if you have them.

                                 If the user tries to do anything other than create or find products, you can respond with
                                 a friendly message that you are here to help them with products and services.

                                 Greet the user and ask them how you can help them today.
                                 """)
    response = Message(text=response.text, timestamp=datetime.now(), sender="bot")
    await websocket.send(response.json())

    async for raw in websocket:
        try:
            logger.info(f"Received: {raw}")
            message = Message.parse_raw(raw)

            response = chat.send_message(message.text)

            logger.info(f"Response: {response}")

            if not response.text:
                response = Message(text="Sorry, I don't understand that.. or something went wrong. Please try again.", timestamp=datetime.now(), sender="bot")
                await websocket.send(response.json())
            else:
                response = Message(text=response.text, timestamp=datetime.now(), sender="bot")
                await websocket.send(response.json())
        except Exception as e:
            logger.error(e)
            await websocket.send("Heyyyy... I am having some trouble with that. Let's try again.")

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

