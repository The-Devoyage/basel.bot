from datetime import datetime, timezone
import logging
from beanie.operators import Set
from fastapi import APIRouter, HTTPException, Header, Request
from fastapi.param_functions import Depends
from classes.user_claims import UserClaims
from database.subscription import Subscription
from utils.environment import get_env_var
import stripe
from stripe import Event

from utils.jwt import require_auth
from utils.responses import create_response

router = APIRouter()

logger = logging.getLogger(__name__)

# Constants
STRIPE_API_KEY = get_env_var("STRIPE_API_KEY")
STRIPE_PRICE_ID = get_env_var("STRIPE_PRICE_ID")
STRIPE_ENDPOINT_SECRET = get_env_var("STRIPE_ENDPOINT_SECRET")
CLIENT_URL = get_env_var("CLIENT_URL")

# Init Stripe
stripe.api_key = STRIPE_API_KEY


@router.get("/subscriptions")
async def get_subscriptions(user_claims: UserClaims = Depends(require_auth)):
    try:
        subscriptions = await Subscription.find_many(
            Subscription.user.id == user_claims.user.id  # type:ignore
        ).to_list()

        return create_response(
            success=True,
            data=[
                await subscription.to_public_dict() for subscription in subscriptions
            ],
        )

    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")


@router.get("/subscribe-start")
async def subscribe_start(user_claims: UserClaims = Depends(require_auth)):
    try:
        subscriptions = await Subscription.find_many(
            Subscription.user == user_claims.user
        ).to_list()

        if subscriptions:
            return create_response(
                success=False,
                message="User is already subscribed.",
                status=403,
            )

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price": STRIPE_PRICE_ID,
                    "quantity": 1,
                },
            ],
            mode="subscription",
            success_url=CLIENT_URL,
            cancel_url=CLIENT_URL,
            customer_email=user_claims.user.email,
        )

        subscription = await Subscription(
            user=user_claims.user,  # type:ignore
            checkout_session_id=checkout_session.id,
            status=False,
            created_by=user_claims.user,  # type:ignore
        ).create()

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
        logger.debug(event)
        if (
            event["type"] == "checkout.session.completed"
            or event["type"] == "checkout.session.async_payment_succeeded"
        ):
            await handle_success_checkout(event)
        if event["type"] == "customer.subscription.updated":
            await handle_subscription_cancel(event)
        return create_response(success=True)
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")


async def handle_success_checkout(event: Event):
    logger.debug("HANDLE SUCCESS CHECKOUT")
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

    try:
        if event["data"]["object"]["canceled_at"]:
            subscriptions = await Subscription.find(
                Subscription.customer_id == event["data"]["object"]["customer"]
            ).to_list()
            if not subscriptions:
                return create_response(success=True)
            for subscription in subscriptions:
                subscription.status = False
                subscription.updated_at = datetime.now(timezone.utc)
                await subscription.save()

        if (
            not event["data"]["object"]["canceled_at"]
            and event["data"]["previous_attributes"]["canceled_at"]
        ):
            subscriptions = await Subscription.find_many(
                Subscription.customer_id == event["data"]["object"]["customer"]
            ).to_list()
            if not subscriptions:
                raise Exception("Customer has no recorded subscriptions.")
            await subscriptions[0].update(Set({"status": True}))
    except Exception as e:
        logger.warn(e)
        return
