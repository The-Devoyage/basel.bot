from typing import Optional
from uuid import UUID
from beanie import SortDirection
from chromadb.api.models.Collection import logging
from fastapi import APIRouter, Depends, HTTPException

from classes.user_claims import UserClaims
from database.interview import Interview, get_pipeline
from database.organization import Organization
from utils.jwt import get_sl_token_claims, optional_auth
from utils.responses import create_response

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/")
async def get_interview(uuid: str):
    try:
        pipeline = get_pipeline(
            user_id=None,
            taken_by_me=False,
            shareable_link_id=None,
        )

        interviews = (
            await Interview.find(
                Interview.uuid == UUID(uuid),
            )
            .aggregate(pipeline)
            .to_list()
        )

        logger.debug(interviews)

        if not interviews:
            return HTTPException(status_code=500, detail="Failed to find interview.")

        interview = interviews[0]

        return create_response(success=True, data=interview)

    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")


@router.get("/list")
async def get_interviews(
    search_term: Optional[str] = None,
    taken_by_me: bool = False,
    organization_uuid: Optional[UUID] = None,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    user_claims: Optional[UserClaims] = Depends(optional_auth),
    sl_token: Optional[str] = None,
):
    try:
        chatting_with = None
        sl_token_claims = None
        organization = None

        query = Interview.find(
            Interview.status == True,
            Interview.deleted_at == None,
        )

        # Get Target User
        if sl_token:
            sl_token_claims = await get_sl_token_claims(sl_token)
            chatting_with = sl_token_claims.chatting_with
        elif user_claims:
            chatting_with = user_claims.user

        if organization_uuid:
            organization = await Organization.find_one(
                Organization.uuid == organization_uuid
            )
            query.find(Interview.organization.id == organization.id)  # type:ignore

        if search_term:
            query.find({"$text": {"$search": search_term}})

        pipeline = get_pipeline(
            user_id=chatting_with.id if chatting_with else None,
            taken_by_me=taken_by_me,
            shareable_link_id=sl_token_claims.shareable_link.id
            if sl_token_claims
            else None,
        )

        total = await query.aggregate(pipeline).to_list()

        interviews = (
            await query.limit(limit)
            .skip(offset)
            .sort([(Interview.created_at, SortDirection.DESCENDING)])  # type:ignore
            .aggregate(pipeline)
            .to_list()
        )

        logger.debug(f"INTS, {interviews}")

        return create_response(
            success=True,
            data=interviews,
            total=len(total),
        )

    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")
