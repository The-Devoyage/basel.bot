import logging
from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from basel.agent import get_agent
from classes.user_claims import UserClaims
from utils.jwt import require_auth
from database.message import Message
from utils.responses import create_response
from utils.subscription import verify_subscription

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/suggest")
async def get_standups(
    user_claims: UserClaims = Depends(require_auth),
):
    try:
        message = (
            await Message.find(
                Message.user.id == user_claims.user.id,  # type:ignore
                Message.sender == "bot",
            )
            .sort("-created_at")
            .first_or_none()
        )

        logger.debug(f"RECENT MESSAGE: {message}")

        if not message:
            raise Exception("Failed to find most recent message.")

        subscription_status = await verify_subscription(
            user_claims.user, user_claims.user.created_at
        )

        agent = await get_agent(
            is_candidate=True,
            chatting_with=user_claims.user,
            user_claims=user_claims,
            subscription_status=subscription_status,
            shareable_link=None,
        )

        response = await agent.achat(
            f"""
            - Use the candidate profile to answer the following question or prompt as if you were the candidate.
            - Respond in first person. 
            - Represent the user accuratly and do not pretend to know things they
            might not know. 
            - If the candidate profile does not contain an answer, politely respod a variation of "i dont know".

            Question/last message:
           {message}
           """
        )

        return create_response(success=True, data={"text": response.response})

    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")
