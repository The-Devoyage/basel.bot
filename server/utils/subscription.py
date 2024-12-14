from datetime import datetime, timedelta, timezone
from typing import List, Optional
from beanie import PydanticObjectId

from pydantic import BaseModel
import logging
from database.subscription import Subscription

from database.user import User

logger = logging.getLogger(__name__)


class SubscriptionStatus(BaseModel):
    subscriptions: Optional[List[Subscription]]
    active: bool
    is_free_trial: bool


async def verify_subscription(
    user: User, user_created_at: datetime
) -> SubscriptionStatus:
    logger.debug("VERIFY SUBSCRIPTION")
    try:
        subscriptions = await Subscription.find(
            Subscription.user.id == user.id,  # type:ignore
        ).to_list()

        logger.debug(f"SUBSCRIPTIONS: {subscriptions}")

        # Handle Active Subscriptions
        if len(subscriptions) > 0:
            active = False
            i = 0
            while i < len(subscriptions) and not active:
                if subscriptions[i].status:
                    active = True
                    break
                i += 1
            if active:
                return SubscriptionStatus(
                    subscriptions=subscriptions, active=active, is_free_trial=False
                )

        # Handle Free Trials
        user_created_at = user_created_at.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        if now < user_created_at + timedelta(days=30):
            return SubscriptionStatus(
                subscriptions=None, is_free_trial=True, active=False
            )

        # Inacive Subscriptions
        return SubscriptionStatus(
            subscriptions=subscriptions, active=False, is_free_trial=False
        )
    except Exception as e:
        logger.error(e)
        raise e
