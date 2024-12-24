from fastapi import APIRouter, HTTPException
from python_http_client.client import logging

from cron.standup import send_daily_standup_reminder
from utils.responses import create_response

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/daily-standup-reminder")
async def daily_standup_reminder():
    try:
        await send_daily_standup_reminder()
        return create_response(success=True)
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")
