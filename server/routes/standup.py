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
from utils.jwt import optional_auth
import jwt

from utils.responses import create_response

logger = logging.getLogger(__name__)

router = APIRouter()

SHAREABLE_LINK_SECRET = get_env_var("SHAREABLE_LINK_SECRET")
ALGORITHM = get_env_var("JWT_ALGORITHM")


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
            decoded = jwt.decode(
                sl_token, SHAREABLE_LINK_SECRET, algorithms=[ALGORITHM]
            )
            sl_claims = cast(ShareableLinkClaims, ShareableLinkClaims(**decoded))
            chatting_with = await User.find_one(User.uuid == UUID(sl_claims.user_uuid))
            shareable_link = await ShareableLink.find_one(
                ShareableLink.uuid == UUID(sl_claims.shareable_link_uuid)
            )
            if not shareable_link:
                logger.error("SHAREABLE LINK TOKEN USER NOT FOUND")
                return HTTPException(
                    status_code=500, detail="Shareable Link Token User Not Found"
                )
            if not shareable_link.status:
                logger.error("SHAREABLE LINK REVOKED")
                return HTTPException(status_code=500, detail="Shareable Link Disabled")

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
