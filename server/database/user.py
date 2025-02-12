import logging
from typing import Optional, Set
from uuid import UUID, uuid4
from beanie import Link
from llama_index.core.bridge.pydantic import Field
from database.base import BaseMongoModel
from database.role import Role
from database.file import File

logger = logging.getLogger(__name__)


class User(BaseMongoModel):
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    role: Link[Role]
    status: bool = False
    auth_id: UUID = Field(default_factory=uuid4)
    profile_image: Optional[Link[File]] = None

    def exclude_from_public_dict(self) -> Set[str]:
        return {"id", "auth_id", "email", "phone"}

    def get_virtual_fields(self) -> dict:
        return {"full_name": self.full_name(), "initials": self.get_first_initial()}

    def full_name(self) -> Optional[str]:
        name = ""
        if self.first_name:
            name += self.first_name
        if self.last_name:
            name += f" {self.last_name}"
        name = name.strip()
        if not name:
            return None
        return name

    def get_first_initial(self) -> str:
        full_name = self.full_name()
        if full_name:
            return full_name[0]
        else:
            return self.email[0] if self.email else ""
