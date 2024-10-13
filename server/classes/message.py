from datetime import datetime
from typing import Literal
from pydantic import BaseModel


class Message(BaseModel):
    text: str
    timestamp: datetime
    sender: Literal["user", "bot"]
