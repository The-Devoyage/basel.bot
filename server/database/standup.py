from typing import Optional

from beanie import Link
from database.base import BaseMongoModel
from database.user import User


class Standup(BaseMongoModel):
    yesterday: Optional[str] = None
    today: Optional[str] = None
    blockers: Optional[str] = None
    user: Link[User]
