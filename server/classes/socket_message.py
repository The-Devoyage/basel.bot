from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from database.message import SenderIdentifer
from database.file import File


class ButtonAction(BaseModel):
    type: str
    endpoint: str


class Button(BaseModel):
    label: str
    action: ButtonAction


class SocketMessage(BaseModel):
    text: str
    timestamp: datetime
    sender: SenderIdentifer
    buttons: Optional[List[Button]] = None
    files: Optional[List[File]] = None
