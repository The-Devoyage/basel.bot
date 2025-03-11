from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

from database.message import ChatMode, SenderIdentifer
from database.file import File


class ButtonAction(BaseModel):
    type: str
    endpoint: str


class Button(BaseModel):
    label: str
    action: ButtonAction


class MessageType(str, Enum):
    MESSAGE = "message"
    END = "end"
    CARD = "card"


class SocketMessage(BaseModel):
    text: str
    timestamp: datetime
    sender: SenderIdentifer
    buttons: Optional[List[Button]] = None
    files: Optional[List[File]] = None
    context: Optional[str] = None
    message_type: MessageType = MessageType.MESSAGE
    chat_mode: ChatMode = ChatMode.CHAT
