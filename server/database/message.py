from enum import Enum
from typing import Optional
from beanie import Link
from database.base import BaseMongoModel
from database.user import User


class SenderIdentifer(str, Enum):
    BOT = "bot"
    USER = "user"


class ChatMode(str, Enum):
    CHAT = "chat"
    INTERVIEW = "interview"


class Message(BaseMongoModel):
    user: Link[User]
    sender: SenderIdentifer
    text: str
    context: Optional[str] = None
    chat_mode: ChatMode = ChatMode.CHAT
