from datetime import datetime
from typing import Literal
from pydantic import BaseModel


class SocketMessage(BaseModel):
    text: str
    timestamp: datetime
    sender: Literal["user", "bot"]
