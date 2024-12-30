from enum import Enum
from beanie import Link
from database.base import BaseMongoModel
from database.user import User


class NotificationType(str, Enum):
    GENERAL = "general"
    META_ADDED = "meta_added"


class Notification(BaseMongoModel):
    user: Link[User]
    text: str
    type: NotificationType
    read: bool = False
