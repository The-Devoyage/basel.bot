from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Interview(BaseModel):
    id: int
    uuid: str
    name: str
    description: str
    status: bool
    created_by: Optional[int]
    updated_by: Optional[int]
    deleted_by: Optional[int]
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    def to_public_dict(self) -> dict:
        interview = self.model_dump(
            exclude={"id", "created_by", "updated_by", "deleted_by"}
        )
        return interview
