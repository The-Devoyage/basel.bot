from typing import Optional, cast
from uuid import UUID
from fastapi import Cookie
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
import logging

from pydantic import BaseModel

from classes.user_claims import ShareableLinkClaims, UserClaims
from database.shareable_link import ShareableLink
from database.token_session import TokenSession
from database.user import User
from utils.environment import get_env_var
from utils.subscription import verify_subscription

logger = logging.getLogger(__name__)

# Constants
ACCESS_SECRET = get_env_var("ACCESS_SECRET")
JWT_ALGO = get_env_var("JWT_ALGORITHM")
ALGORITHM = get_env_var("JWT_ALGORITHM")
SHAREABLE_LINK_SECRET = get_env_var("SHAREABLE_LINK_SECRET")
ALGORITHM = get_env_var("JWT_ALGORITHM")


oauth2scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_jwt(payload: dict, secret: str) -> str:
    """Create a JWT token."""
    return jwt.encode(payload, secret, algorithm=ALGORITHM)


async def handle_decode_token(token: str) -> UserClaims:
    """Decode a JWT token."""
    logger.debug("DECODING JWT")
    try:
        decoded_token = jwt.decode(token, ACCESS_SECRET, algorithms=[ALGORITHM])
        # Populate User Service Context
        user = await User.find_one(User.uuid == UUID(decoded_token["user_uuid"]))
        if not user:
            raise Exception("User not found")
        subscription_status = await verify_subscription(user)
        decoded_token["user"] = user
        decoded_token["subscription_status"] = subscription_status
        return cast(UserClaims, UserClaims(**decoded_token))
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")


async def verify_token_session(token_session_uuid: str) -> bool:
    """Verify a token session."""
    logger.debug("VERIFY TOKEN SESSION")
    try:
        token_session = await TokenSession.find_one(
            TokenSession.uuid == UUID(token_session_uuid)
        )
        if not token_session:
            logger.error("NO TOKEN SESSION FOUND")
            raise HTTPException(status_code=401, detail="Token session not found")
        if token_session.status is False:
            logger.error("TOKEN SESSION IS INVALID")
            raise HTTPException(status_code=401, detail="Token session is invalid")
        return True
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=401, detail="Invalid token")


async def optional_auth(token: Optional[str] = Cookie(None)) -> Optional[UserClaims]:
    """Verify a Optional JWT token."""
    logger.debug(f"Optional Token: {token}")
    if not token:
        return None
    user_claims = await handle_decode_token(token)
    return user_claims


async def require_auth(token: str = Cookie(None)) -> UserClaims:
    """Verify a JWT token."""
    logger.debug(f"Token: {token}")
    user_claims = await handle_decode_token(token)
    await verify_token_session(user_claims.token_session_uuid)
    return user_claims


class GetSlTokenClaims(BaseModel):
    chatting_with: User
    shareable_link: ShareableLink
    sl_claims: ShareableLinkClaims


async def get_sl_token_claims(sl_token: str) -> GetSlTokenClaims:
    try:
        decoded = jwt.decode(sl_token, SHAREABLE_LINK_SECRET, algorithms=[ALGORITHM])
        sl_claims = cast(ShareableLinkClaims, ShareableLinkClaims(**decoded))
        chatting_with = await User.find_one(User.uuid == UUID(sl_claims.user_uuid))
        shareable_link = await ShareableLink.find_one(
            ShareableLink.uuid == UUID(sl_claims.shareable_link_uuid)
        )
        if not shareable_link:
            logger.error("SHAREABLE LINK TOKEN USER NOT FOUND")
            raise HTTPException(status_code=500, detail="Shareable Link Not Found")
        if not shareable_link.status:
            logger.error("SHAREABLE LINK REVOKED")
            raise HTTPException(status_code=500, detail="Shareable Link Disabled")
        if not chatting_with:
            logger.error("SHAREABLE LINK USER NOT FOUND")
            raise HTTPException(status_code=500, detail="SL User Not Found.")

        return GetSlTokenClaims(
            chatting_with=chatting_with,
            shareable_link=shareable_link,
            sl_claims=sl_claims,
        )

    except jwt.DecodeError as e:
        logger.error(f"Invalid token: {e}")
        raise HTTPException(status_code=400, detail="Invalid token")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
