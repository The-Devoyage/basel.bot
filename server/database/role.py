from enum import Enum

from database.base import BaseMongoModel


# Define an Enum for the `identifier` field
class RoleIdentifier(str, Enum):
    ADMIN = "admin"
    USER = "user"


class Role(BaseMongoModel):
    identifier: RoleIdentifier
    name: str
