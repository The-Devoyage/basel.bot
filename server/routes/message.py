from typing import Optional
from beanie import SortDirection
from fastapi import APIRouter, Depends, HTTPException
import logging
from classes.user_claims import UserClaims

from database.message import Message
from utils.jwt import require_auth
from utils.responses import create_response

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/list")
async def get_messages(
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    user_claims: UserClaims = Depends(require_auth),
):
    try:
        messages = (
            await Message.find(
                Message.created_by.id  # type:ignore
                == user_claims.user.id
            )
            .limit(limit)
            .skip(offset)
            .sort([(Message.created_at, SortDirection.DESCENDING)])  # type:ignore
            .to_list()
        )

        messages.reverse()

        return create_response(
            success=True, data=[await m.to_public_dict() for m in messages]
        )

    except Exception as e:
        logger.debug(e)
        return HTTPException(status_code=500, detail="Something went wrong...")
