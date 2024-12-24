from fastapi import HTTPException, Header
from python_http_client.client import logging
from utils.environment import get_env_var
from fastapi.security import APIKeyHeader

logger = logging.getLogger(__name__)

# Constants
CRON_API_KEY = get_env_var("CRON_API_KEY")

header_scheme = APIKeyHeader(name="x-mailer-api-key")


async def require_api_key(api_key: str = Header()) -> str:
    """Verify a JWT token."""
    logger.debug("VERIFY API KEY")
    if api_key != CRON_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return api_key
