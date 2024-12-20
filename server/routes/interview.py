from typing import Optional
from chromadb.api.models.Collection import logging
from fastapi import APIRouter, Depends, HTTPException

from classes.user_claims import UserClaims
from database.interview import Interview
from utils.jwt import require_auth
from utils.responses import create_response

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/interviews")
async def get_interviews(
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    _: UserClaims = Depends(require_auth),
):
    try:
        interviews = await Interview.find().limit(limit).skip(offset).to_list()
        return create_response(
            success=True,
            data=[await interview.to_public_dict() for interview in interviews],
        )

    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")
