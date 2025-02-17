from enum import Enum
from typing import Optional
from datetime import datetime
from beanie import Link
from database.base import BaseMongoModel
from database.user import User


class SubscriptionTier(str, Enum):
    CANDIDATE = "candidate"
    CANDIDATE_PRO = "candidate_pro"
    ORGANIZATION = "organization"


class Subscription(BaseMongoModel):
    user: Link[User]
    customer_id: Optional[str] = None
    checkout_session_id: str
    tier: SubscriptionTier = SubscriptionTier.CANDIDATE
    canceled_at: Optional[datetime] = None
    cancel_at: Optional[datetime] = None
    status: bool
