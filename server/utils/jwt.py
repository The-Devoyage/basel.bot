from typing import cast
from fastapi import Cookie
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
import logging

from classes.user_claims import UserClaims
from database.token_session import TokenSessionModel
from database.user import UserModel
from utils.environment import get_env_var

logger = logging.getLogger(__name__)

# Constants
ACCESS_SECRET = get_env_var("ACCESS_SECRET")
JWT_ALGO = get_env_var("JWT_ALGORITHM")
ALGORITHM = get_env_var("JWT_ALGORITHM")

oauth2scheme = OAuth2PasswordBearer(tokenUrl="token")

# Database
token_session_model = TokenSessionModel("basel.db")
user_model = UserModel("basel.db")


def create_jwt(payload: dict, secret: str) -> str:
    """Create a JWT token."""
    return jwt.encode(payload, secret, algorithm=ALGORITHM)


def handle_decode_token(token: str) -> UserClaims:
    """Decode a JWT token."""
    try:
        decoded_token = jwt.decode(token, ACCESS_SECRET, algorithms=[ALGORITHM])
        conn = user_model._get_connection()
        cursor = conn.cursor()
        user = user_model.get_user_by_uuid(cursor, decoded_token["user_uuid"])
        if not user:
            raise Exception("User not found")
        decoded_token["user"] = user
        return cast(UserClaims, UserClaims(**decoded_token))
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")


def verify_token_session(token_session_uuid: str) -> bool:
    """Verify a token session."""
    connection = token_session_model._get_connection()
    cursor = connection.cursor()
    try:
        token_session = token_session_model.get_token_session_by_uuid(
            cursor, token_session_uuid
        )
        logger.debug(f"Token session: {token_session}")

        if not token_session:
            raise HTTPException(status_code=401, detail="Token session not found")
        if token_session.status is False:
            raise HTTPException(status_code=401, detail="Token session is invalid")
        return True
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=401, detail="Invalid token")


def require_auth(token: str = Cookie(None)) -> UserClaims:
    """Verify a JWT token."""
    logger.debug(f"Token: {token}")
    user_claims = handle_decode_token(token)
    verify_token_session(user_claims.token_session_uuid)
    return user_claims
