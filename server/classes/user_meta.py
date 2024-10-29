from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class UserMeta(BaseModel):
    id: int
    user_id: int
    data: str
    tags: Optional[str]
    created_by: int
    updated_by: int
    deleted_by: Optional[int]
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    def to_public_dict(self) -> dict:
        return self.model_dump(exclude={"id", "created_by", "updated_by", "deleted_by"})
