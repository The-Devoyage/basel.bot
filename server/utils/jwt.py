import os
import jwt
from dotenv import load_dotenv

load_dotenv()

algorithm = os.getenv("JWT_ALGORITHM")
if not algorithm:
    raise ValueError("JWT_ALGORITHM environment variable not set")


def create_jwt(payload: dict, secret: str) -> str:
    """Create a JWT token."""
    return jwt.encode(payload, secret, algorithm=algorithm)
