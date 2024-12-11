from typing import Optional
from beanie import Link
from database.base import BaseMongoModel

from database.user import User


class UserMeta(BaseMongoModel):
    user: Link[User]
    data: str
    tags: Optional[str] = None
