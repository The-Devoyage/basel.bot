from datetime import datetime, timedelta, timezone
from database.subscription import SubscriptionModel
import logging

logger = logging.getLogger(__name__)

subscription_model = SubscriptionModel("basel.db")


def verify_subscription(user_id: int, user_created_at: datetime):
    user_created_at = user_created_at.replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    if now < user_created_at + timedelta(days=30):
        return True

    try:
        conn = subscription_model._get_connection()
        cursor = conn.cursor()
        subscriptions = subscription_model.get_subscriptions_by_user_id(cursor, user_id)
        logger.debug(f"USER SUBSCRIPTIONS: {subscriptions}")
        if not subscriptions:
            return False
        return True
    except Exception as e:
        logger.error(e)
        raise e
