from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class Subscription(BaseModel):
    id: int
    uuid: str
    user_id: int
    status: bool
    created_by: Optional[int]
    updated_by: Optional[int]
    deleted_by: Optional[int]
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    def to_public_dict(self) -> dict:
        subscription = self.model_dump(
            exclude={"id", "created_by", "updated_by", "deleted_by"}
        )

        return subscription
