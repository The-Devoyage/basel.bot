from typing import Optional

from beanie import Link

from database.base import BaseMongoModel
from database.user import User


class Subscription(BaseMongoModel):
    user: Link[User]
    customer_id: Optional[str] = None
    checkout_session_id: str
    status: bool
