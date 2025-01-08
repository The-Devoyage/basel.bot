import logging
from datetime import datetime
from typing import Optional
from classes.user_claims import UserClaims
from database.standup import Standup
from fastapi import APIRouter, Depends, HTTPException
from utils.jwt import require_auth

from utils.responses import create_response

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/standups")
async def get_standups(
    start_date: datetime,
    end_date: datetime,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    user_claims: UserClaims = Depends(require_auth),
):
    try:
        standups = (
            await Standup.find(
                Standup.user.id == user_claims.user.id,  # type:ignore
                Standup.created_at >= start_date,
                Standup.created_at <= end_date,
            )
            .limit(limit)
            .skip(offset)
            .to_list()
        )
        return create_response(
            success=True, data=[await standup.to_public_dict() for standup in standups]
        )

    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")
