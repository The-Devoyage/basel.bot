from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class Message(BaseModel):
    id: int
    uuid: str
    user_id: int
    sender: str
    text: str
    created_by: Optional[int]
    updated_by: Optional[int]
    deleted_by: Optional[int]
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    def to_public_dict(self) -> dict:
        return self.model_dump(exclude={"id", "created_by", "updated_by", "deleted_by"})
