from enum import Enum
from beanie import Link
from database.base import BaseMongoModel
from database.user import User


class SenderIdentifer(str, Enum):
    BOT = "bot"
    USER = "user"


class Message(BaseMongoModel):
    user: Link[User]
    sender: SenderIdentifer
    text: str
