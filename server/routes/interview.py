from typing import List, Optional
from beanie import SortDirection
from chromadb.api.models.Collection import logging
from fastapi import APIRouter, Depends, HTTPException

from classes.user_claims import UserClaims
from database.interview import Interview, get_pipeline
from utils.jwt import optional_auth
from utils.responses import create_response

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/interviews")
async def get_interviews(
    search_term: Optional[str] = None,
    tags: Optional[List[str]] = None,
    url: Optional[str] = None,
    created_by_me: Optional[bool] = None,
    taken_by_me: bool = False,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    user_claims: Optional[UserClaims] = Depends(optional_auth),
):
    try:
        query = Interview.find(
            Interview.status == True,
            Interview.deleted_at == None,
        )

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

        pipeline = get_pipeline(user_claims, taken_by_me)

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
