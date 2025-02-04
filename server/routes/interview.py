from typing import List, Optional
from uuid import UUID
from beanie import SortDirection
from chromadb.api.models.Collection import logging
from fastapi import APIRouter, Depends, HTTPException

from classes.user_claims import UserClaims
from database.interview import Interview, get_pipeline
from utils.jwt import get_sl_token_claims, optional_auth
from utils.responses import create_response

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/")
async def get_interview(uuid: str):
    try:
        interview = await Interview.find_one(Interview.uuid == UUID(uuid))

        if not interview:
            return create_response(success=False)

        return create_response(success=True, data=await interview.to_public_dict())

    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")


@router.get("/list")
async def get_interviews(
    search_term: Optional[str] = None,
    tags: Optional[List[str]] = None,
    url: Optional[str] = None,
    created_by_me: Optional[bool] = None,
    taken_by_me: bool = False,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    user_claims: Optional[UserClaims] = Depends(optional_auth),
    sl_token: Optional[str] = None,
):
    try:
        query = Interview.find(
            Interview.status == True,
            Interview.deleted_at == None,
        )

        chatting_with = None
        sl_token_claims = None
        if sl_token:
            sl_token_claims = await get_sl_token_claims(sl_token)
            chatting_with = sl_token_claims.chatting_with
        elif user_claims:
            chatting_with = user_claims.user

        if search_term:
            query.find({"$text": {"$search": search_term}})
        if tags:
            tags_query = [{"tags": {"$regex": tag, "$options": "i"}} for tag in tags]
            query.find({"$or": tags_query})
        if url:
            query.find({"url": url})
        if created_by_me is not None:
            if created_by_me:
                query.find(
                    Interview.created_by.id == user_claims.user.id,  # type:ignore
                    fetch_links=True,
                )
            else:
                query.find(
                    Interview.created_by.id != user_claims.user.id,  # type:ignore
                    fetch_links=True,
                )

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

        return create_response(
            success=True,
            data=interviews,
            total=len(total),
        )

    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")
