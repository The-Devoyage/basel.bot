from datetime import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel


class ButtonAction(BaseModel):
    type: str
    endpoint: str


class Button(BaseModel):
    label: str
    action: ButtonAction


class SocketMessage(BaseModel):
    text: str
    timestamp: datetime
    sender: Literal["user", "bot"]
    buttons: Optional[List[Button]] = None
