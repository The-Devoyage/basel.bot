from beanie import Link

from database.base import BaseMongoModel
from database.user import User


class TokenSession(BaseMongoModel):
    user: Link[User]
    status: bool = True
