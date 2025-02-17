from enum import Enum
from typing import List, Optional
from datetime import datetime
from beanie import Link
from database.base import BaseMongoModel


class SubscriptionTier(str, Enum):
    CANDIDATE = "candidate"
    CANDIDATE_PRO = "candidate_pro"
    ORGANIZATION = "organization"


class SubscriptionFeatures(str, Enum):
    CREATE_INTERVIEW = "create_interview"
    UNLIMITED_MEMORIES = "unlimited_metas"
    MANAGE_MEMORIES = "manage_memories"
    MANAGE_ORGANIZATION = "manage_organization"


TIER_FEATURES = {
    SubscriptionTier.CANDIDATE: [],
    SubscriptionTier.CANDIDATE_PRO: [
        SubscriptionFeatures.CREATE_INTERVIEW,
        SubscriptionFeatures.UNLIMITED_MEMORIES,
        SubscriptionFeatures.MANAGE_MEMORIES,
    ],
    SubscriptionTier.ORGANIZATION: [
        SubscriptionFeatures.CREATE_INTERVIEW,
        SubscriptionFeatures.UNLIMITED_MEMORIES,
        SubscriptionFeatures.MANAGE_MEMORIES,
        SubscriptionFeatures.MANAGE_ORGANIZATION,
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
    features: List[SubscriptionFeatures] = TIER_FEATURES[SubscriptionTier.CANDIDATE]
