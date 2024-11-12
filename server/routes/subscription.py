import logging
from fastapi import APIRouter, HTTPException, Header
from fastapi.param_functions import Depends
from classes.user_claims import UserClaims
from database.subscription import SubscriptionModel
from utils.environment import get_env_var
import stripe

from utils.jwt import require_auth
from utils.responses import create_response

router = APIRouter()

logger = logging.getLogger(__name__)

# Constants
STRIPE_API_KEY = get_env_var("STRIPE_API_KEY")
STRIPE_PRICE_ID = get_env_var("STRIPE_PRICE_ID")
STRIPE_ENDPOINT_SECRET = get_env_var("STRIPE_ENDPOINT_SECRET")
CLIENT_URL = get_env_var("CLIENT_URL")

# Models
subscription_model = SubscriptionModel("basel.db")

# Init Stripe
stripe.api_key = STRIPE_API_KEY


@router.get("/subscribe-start")
async def subscribe_start(_: UserClaims = Depends(require_auth)):
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price": STRIPE_PRICE_ID,
                    "quantity": 1,
                },
            ],
            mode="subscription",
            success_url=CLIENT_URL + "/order?success=true",
            cancel_url=CLIENT_URL + "/order?canceled=true",
        )
        return create_response(success=True, data=checkout_session)
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")


@router.post("/subscribe-finish")
async def subscribe_finish(
    payload: dict,
    user_claims: UserClaims = Depends(require_auth),
    stripe_signature: str = Header(None),
):
    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, STRIPE_ENDPOINT_SECRET
        )
        if (
            event["type"] == "checkout.session.completed"
            or event["type"] == "checkout.session.async_payment_succeeded"
        ):
            checkout_session = stripe.checkout.Session.retrieve(
                event["data"]["object"]["id"],
                expand=["line_items"],
            )
            if checkout_session.payment_status != "unpaid":
                # Create subscription
                conn = subscription_model._get_connection()
                cursor = conn.cursor()
                subscription_id = subscription_model.create_subscription(
                    cursor, user_claims.user.id
                )
                conn.commit()
                if not subscription_id:
                    raise Exception("Failed to create subscription.")
                subscription = subscription_model.get_subscription_by_id(
                    cursor, subscription_id
                )
                if not subscription:
                    raise Exception("Failed to find subscription.")
                return create_response(success=True, data=subscription.to_public_dict())
            else:
                raise Exception("Failed to verify payment.")
        else:
            raise Exception("Invalid event.")
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")
