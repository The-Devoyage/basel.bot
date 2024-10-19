import os
from typing import Optional, cast
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from dotenv import load_dotenv
import logging

from classes.user_claims import UserClaims
from utils.environment import get_env_var

load_dotenv()
logger = logging.getLogger(__name__)

ACCESS_SECRET = get_env_var("ACCESS_SECRET")
JWT_ALGO = get_env_var("JWT_ALGORITHM")

algorithm = os.getenv("JWT_ALGORITHM")
if not algorithm:
    raise ValueError("JWT_ALGORITHM environment variable not set")


def create_jwt(payload: dict, secret: str) -> str:
    """Create a JWT token."""
    return jwt.encode(payload, secret, algorithm=algorithm)


oauth2scheme = OAuth2PasswordBearer(tokenUrl="token")


def handle_decode_token(token: str) -> UserClaims:
    """Decode a JWT token."""
    try:
        decoded_token = jwt.decode(token, ACCESS_SECRET, algorithms=[algorithm])
        return cast(UserClaims, UserClaims(**decoded_token))
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")


def require_auth(token: str = Depends(oauth2scheme)) -> UserClaims:
    """Verify a JWT token."""
    return handle_decode_token(token)
