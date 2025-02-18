from datetime import datetime, timezone
import logging
from beanie.operators import Set
from fastapi import APIRouter, HTTPException, Header, Request
from fastapi.param_functions import Depends
from classes.user_claims import UserClaims
from database.subscription import TIER_FEATURES, Subscription, SubscriptionTier
from utils.environment import get_env_var
import stripe
from stripe import Event
from utils.subscription import get_tier_by_price, TIER_PRICE_ID, verify_subscription

from utils.jwt import require_auth
from utils.responses import create_response

router = APIRouter()

logger = logging.getLogger(__name__)

# Constants
STRIPE_API_KEY = get_env_var("STRIPE_API_KEY")
STRIPE_ENDPOINT_SECRET = get_env_var("STRIPE_ENDPOINT_SECRET")
CLIENT_URL = get_env_var("CLIENT_URL")

# Init Stripe
stripe.api_key = STRIPE_API_KEY


@router.get("/subscription-status")
async def get_subscription(user_claims: UserClaims = Depends(require_auth)):
    try:
        subscription_status = await verify_subscription(user_claims.user)

        return create_response(
            success=True, data=await subscription_status.to_public_dict()
        )
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail=str(e))


@router.get("/subscribe-start")
async def subscribe_start(
    tier: SubscriptionTier, user_claims: UserClaims = Depends(require_auth)
):
    try:
        # Check if the user is subscribed.
        subscription = await Subscription.find_one(
            Subscription.user.id == user_claims.user.id,  # type:ignore
            Subscription.status == True,
        )
        if subscription:
            return create_response(
                success=False,
                message="User is already subscribed.",
                status=403,
            )

        selected_tier = TIER_PRICE_ID.get(tier)

        if not selected_tier:
            return create_response(
                success=False, message="Invalid tier selected.", status=403
            )

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price": selected_tier,
                    "quantity": 1,
                },
            ],
            mode="subscription",
            success_url=CLIENT_URL,
            cancel_url=CLIENT_URL,
            customer_email=user_claims.user.email,
        )

        subscription = await Subscription.find_one(
            Subscription.user.id == user_claims.user.id,  # type:ignore
        ).upsert(
            Set({"checkout_session_id": checkout_session.id}),
            on_insert=Subscription(
                user=user_claims.user,  # type:ignore
                checkout_session_id=checkout_session.id,
                status=False,
                created_by=user_claims.user,  # type:ignore
                updated_by=user_claims.user,  # type:ignore
                tier=tier,
            ),
        )

        if not subscription:
            raise Exception("Failed to create subscription.")

        return create_response(success=True, data={"url": checkout_session.url})
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")


@router.post("/subscribe-event")
async def subscribe_finish(
    request: Request,
    stripe_signature: str = Header(None),
):
    """Webhook from stripe to activate the subscription."""
    payload = await request.body()
    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, STRIPE_ENDPOINT_SECRET
        )

        event_data = event["data"]["object"]

        # Handle New Subscriptions
        if (
            event.type == "checkout.session.completed"
            or event.type == "checkout.session.async_payment_succeeded"
        ):
            await handle_success_checkout(event)

        if (
            event.type == "customer.subscription.updated"
            and "items" in event_data
            and not event_data["canceled_at"]
            and not event_data.get("previous_attributes", {"canceled_at": None})[
                "canceled_at"
            ]
        ):
            await handle_plan_change(event)

        # Handle Cancelled Subscriptions
        if event.type == "customer.subscription.updated" and event_data["canceled_at"]:
            await handle_subscription_cancel(event)

        # # Handle Reactivations
        if (
            event.type == "customer.subscription.updated"
            and not event_data["canceled_at"]
            and event["data"]["previous_attributes"]["canceled_at"]
        ):
            await handle_subscription_reactivate(event)
            return create_response(success=True)

        return create_response(success=False)

    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")


async def handle_success_checkout(event: Event):
    logger.debug("HANDLE SUCCESS CHECKOUT")
    logger.debug(event)

    checkout_session = stripe.checkout.Session.retrieve(
        event["data"]["object"]["id"],
        expand=["line_items"],
    )
    if checkout_session.payment_status != "unpaid":
        # Create subscription
        subscription = await Subscription.find_one(
            Subscription.checkout_session_id == checkout_session.id
        )

        if not subscription:
            raise Exception("Subscription not found.")

        subscription.status = True
        subscription.customer_id = event["data"]["object"]["customer"]
        subscription.updated_at = datetime.now(timezone.utc)

        await subscription.save()

        if not subscription:
            raise Exception("Failed to retrieve updated subscription information.")
        return create_response(success=True)

    else:
        raise Exception("Failed to verify payment.")


async def handle_subscription_cancel(event: Event):
    logger.debug("HANDLE CANCEL")
    logger.debug(event)

    try:
        subscription = await Subscription.find_one(
            Subscription.customer_id == event["data"]["object"]["customer"]
        )
        if not subscription:
            return create_response(success=True)
        subscription.status = False
        subscription.updated_at = datetime.now(timezone.utc)
        subscription.cancel_at = datetime.utcfromtimestamp(
            event["data"]["object"]["cancel_at"]
        )
        subscription.canceled_at = datetime.utcfromtimestamp(
            event["data"]["object"]["canceled_at"]
        )
        await subscription.save()
    except Exception as e:
        logger.warn(e)
        return


async def handle_subscription_reactivate(event: Event):
    logger.debug("HANDLE REACTIVATE")
    logger.debug(event)

    try:
        subscription = await Subscription.find_one(
            Subscription.customer_id == event["data"]["object"]["customer"]
        )

        if not subscription:
            raise Exception("Customer has no recorded subscriptions.")
        subscription.status = True
        subscription.cancel_at = None
        subscription.canceled_at = None
        await subscription.save()
    except Exception as e:
        logger.warn(e)
        return


async def handle_plan_change(event: Event):
    logger.debug("HANDLE PLAN CHANGE")
    logger.debug(event)

    try:
        customer_id = event["data"]["object"]["customer"]
        new_plan_id = event["data"]["object"]["items"]["data"][0]["price"]["id"]
        new_tier = get_tier_by_price(new_plan_id)

        if not new_tier:
            raise Exception("New Tier not valid.")

        # Find the user's subscription
        subscription = await Subscription.find_one(
            Subscription.customer_id == customer_id, Subscription.status == True
        )

        if not subscription:
            raise Exception("Subscription not found.")

        previous_plan_id = TIER_PRICE_ID.get(subscription.tier)

        if not new_plan_id or new_plan_id == previous_plan_id:
            logger.debug("No plan change detected.")
            return create_response(success=True)

        # Update the plan
        # subscription.plan_id = new_plan_id
        subscription.updated_at = datetime.now(timezone.utc)
        subscription.tier = new_tier
        subscription.features = TIER_FEATURES[new_tier]

        await subscription.save()

        logger.debug(f"Subscription updated: {previous_plan_id} -> {new_plan_id}")
        return create_response(success=True)

    except Exception as e:
        logger.warn(f"Error handling plan change: {e}")
        return create_response(success=False)
