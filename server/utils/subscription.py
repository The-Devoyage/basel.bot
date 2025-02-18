from datetime import datetime, timedelta, timezone
from typing import Optional
from pydantic import BaseModel
import logging
from database.subscription import Subscription, SubscriptionFeature, SubscriptionTier
from utils.environment import get_env_var
from database.user import User
from utils.environment import get_env_var

logger = logging.getLogger(__name__)

STRIPE_PRICE_CANIDATE = get_env_var("STRIPE_PRICE_CANDIDATE")
STRIPE_PRICE_CANIDATE_PRO = get_env_var("STRIPE_PRICE_CANDIDATE_PRO")
STRIPE_PRICE_ORGANIZATION = get_env_var("STRIPE_PRICE_ORGANIZATION")


class SubscriptionStatus(BaseModel):
    subscription: Optional[Subscription]
    active: bool
    is_free_trial: bool
    free_trial_expires: Optional[datetime] = None

    async def to_public_dict(self):
        subscription = (
            await self.subscription.to_public_dict() if self.subscription else None
        )
        public_dict = self.model_dump()
        public_dict["subscription"] = subscription
        return public_dict


async def verify_subscription(user: User) -> SubscriptionStatus:
    logger.debug("VERIFY SUBSCRIPTION")
    now = datetime.now(timezone.utc)

    try:
        subscription = await Subscription.find_one(
            Subscription.user.id == user.id,  # type:ignore
        )

        logger.debug(f"SUBSCRIPTION: {subscription}")

        # Handle Active Subscriptions
        if subscription and (
            subscription.status
            or (
                subscription.cancel_at
                and subscription.cancel_at.replace(tzinfo=timezone.utc) > now
            )
        ):
            logger.debug("ACTIVE SUBSCRIPTION")
            return SubscriptionStatus(
                subscription=subscription,
                active=True,
                is_free_trial=False,
            )

        # Handle Free Trials
        user_created_at = user.created_at.replace(tzinfo=timezone.utc)
        free_trial_expires = user_created_at + timedelta(days=30)
        if now < user_created_at + timedelta(days=30):
            logger.debug("FREE TRIAL SUBSCRIPTION")
            return SubscriptionStatus(
                subscription=None,
                is_free_trial=True,
                active=False,
                free_trial_expires=free_trial_expires,
            )

        # Default to Inacive Subscription
        logger.debug("INACTIVE SUBSCRIPTION")
        return SubscriptionStatus(
            subscription=subscription, active=False, is_free_trial=False
        )
    except Exception as e:
        logger.error(e)
        raise e


TIER_PRICE_ID = {
    SubscriptionTier.CANDIDATE: STRIPE_PRICE_CANIDATE,
    SubscriptionTier.CANDIDATE_PRO: STRIPE_PRICE_CANIDATE_PRO,
    SubscriptionTier.ORGANIZATION: STRIPE_PRICE_ORGANIZATION,
}


def get_tier_by_price(price_id: str):
    for tier, stripe_price in TIER_PRICE_ID.items():
        if stripe_price == price_id:
            return tier
    return None


def check_subscription_permission(
    subscription_status: SubscriptionStatus,
    subscription_feature: SubscriptionFeature,
):
    if subscription_status.is_free_trial:
        return True
    if not subscription_status.active:
        return False
    if (
        subscription_status.active
        and subscription_status.subscription
        and subscription_feature in subscription_status.subscription.features
    ):
        return True

    return False
