from typing import Optional
import uuid

from beanie import Link

from database.base import BaseMongoModel
from database.role import Role


class User(BaseMongoModel):
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    role: Link[Role]
    status: bool = False
    auth_id: uuid.UUID = uuid.uuid4()

    def to_public_dict(self) -> dict:
        return self.model_dump(exclude={"_id", "auth_id"})
