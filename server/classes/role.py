from pydantic import BaseModel
from enum import Enum


# Define an Enum for the `identifier` field
class RoleIdentifier(str, Enum):
    ADMIN = "admin"
    USER = "user"


# Define an Enum for the `name` field
class RoleName(str, Enum):
    ADMIN = "Admin"
    USER = "user"


class Role(BaseModel):
    id: int
    identifier: RoleIdentifier
    name: RoleName

    def to_public_dict(self) -> dict:
        # Convert model to a dictionary, excluding the `id` field
        return self.model_dump(exclude={"id"})
