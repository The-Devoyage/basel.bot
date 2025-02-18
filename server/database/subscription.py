from enum import Enum
from typing import List, Optional
from datetime import datetime
from beanie import Link
from database.base import BaseMongoModel


class SubscriptionTier(str, Enum):
    CANDIDATE = "candidate"
    CANDIDATE_PRO = "candidate_pro"
    ORGANIZATION = "organization"


class SubscriptionFeature(str, Enum):
    CREATE_INTERVIEW = "create_interview"
    MANAGE_MEMORIES = "manage_memories"
    MANAGE_ORGANIZATION = "manage_organization"
    LOG_STANDUP = "log_standup"


TIER_FEATURES = {
    SubscriptionTier.CANDIDATE: [],
    SubscriptionTier.CANDIDATE_PRO: [
        SubscriptionFeature.CREATE_INTERVIEW,
        SubscriptionFeature.MANAGE_MEMORIES,
        SubscriptionFeature.LOG_STANDUP,
    ],
    SubscriptionTier.ORGANIZATION: [
        SubscriptionFeature.CREATE_INTERVIEW,
        SubscriptionFeature.MANAGE_MEMORIES,
        SubscriptionFeature.MANAGE_ORGANIZATION,
        SubscriptionFeature.LOG_STANDUP,
    ],
}


class Subscription(BaseMongoModel):
    user: Link["User"]  # type:ignore
    customer_id: Optional[str] = None
    checkout_session_id: str
    tier: SubscriptionTier = SubscriptionTier.CANDIDATE
    canceled_at: Optional[datetime] = None
    cancel_at: Optional[datetime] = None
    status: bool
    features: List[SubscriptionFeature] = TIER_FEATURES[SubscriptionTier.CANDIDATE]
