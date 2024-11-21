from datetime import datetime, timedelta, timezone
from typing import List, Optional

from pydantic import BaseModel
from classes.subscription import Subscription
from database.subscription import SubscriptionModel
import logging

logger = logging.getLogger(__name__)

subscription_model = SubscriptionModel("basel.db")


class SubscriptionStatus(BaseModel):
    subscriptions: Optional[List[Subscription]]
    active: bool
    is_free_trial: bool


def verify_subscription(user_id: int, user_created_at: datetime) -> SubscriptionStatus:
    try:
        conn = subscription_model._get_connection()
        cursor = conn.cursor()
        subscriptions = subscription_model.get_subscriptions_by_user_id(cursor, user_id)

        if len(subscriptions) > 0:
            active = False
            i = 0
            while i < len(subscriptions) and not active:
                if subscriptions[i].status:
                    active = True
                    break
                i += 1
            return SubscriptionStatus(
                subscriptions=subscriptions, active=active, is_free_trial=False
            )

        user_created_at = user_created_at.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        if now < user_created_at + timedelta(days=30):
            return SubscriptionStatus(
                subscriptions=None, is_free_trial=True, active=False
            )

        return SubscriptionStatus(
            subscriptions=subscriptions, active=False, is_free_trial=False
        )
    except Exception as e:
        logger.error(e)
        raise e
