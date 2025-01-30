import logging
from datetime import datetime
from typing import Optional, cast
from uuid import UUID
from classes.user_claims import ShareableLinkClaims, UserClaims
from database.shareable_link import ShareableLink
from database.standup import Standup
from fastapi import APIRouter, Depends, HTTPException
from database.user import User
from utils.environment import get_env_var
from utils.jwt import get_sl_token_claims, optional_auth
import jwt

from utils.responses import create_response

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/standups")
async def get_standups(
    start_date: datetime,
    end_date: datetime,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    user_claims: UserClaims = Depends(optional_auth),
    sl_token: Optional[str] = None,
):
    try:
        sl_claims = None
        chatting_with = None
        if sl_token:
            sl_token_claims = await get_sl_token_claims(sl_token)
            sl_claims = sl_token_claims.sl_claims
            chatting_with = sl_token_claims.chatting_with

        if not sl_claims and not user_claims:
            logger.error("AUTHENTICATION REQUIRED")
            return HTTPException(status_code=500, detail="Authentication Required.")

        query = Standup.find(
            Standup.created_at >= start_date,
            Standup.created_at <= end_date,
        )

        if sl_claims:
            query.find(
                Standup.user.id == chatting_with.id  # type:ignore
            )
        else:
            query.find(
                Standup.user.id == user_claims.user.id,  # type:ignore
            )

        standups = await query.limit(limit).skip(offset).to_list()

        return create_response(
            success=True, data=[await standup.to_public_dict() for standup in standups]
        )

    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")
