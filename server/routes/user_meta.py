from datetime import datetime
import logging
from typing import Optional
from uuid import UUID
from beanie import SortDirection
from fastapi import APIRouter, Depends, HTTPException
from llama_index.core.bridge.pydantic import BaseModel

from classes.user_claims import UserClaims
from database.user_meta import UserMeta
from utils.jwt import require_auth
from utils.responses import create_response


router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/user-metas")
async def get_user_metas(
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    user_claims: UserClaims = Depends(require_auth),
):
    try:
        user_metas = (
            await UserMeta.find(
                UserMeta.user.id  # type:ignore
                == user_claims.user.id,
                UserMeta.deleted_at == None,
                fetch_links=True,
            )
            .sort(
                [(UserMeta.created_at, SortDirection.DESCENDING)]  # type:ignore
            )
            .limit(limit)
            .skip(offset)
            .to_list()
        )
        count = await UserMeta.find(
            UserMeta.user.id == user_claims.user.id  # type:ignore
        ).count()
        logger.debug(f"USER METAS: {user_metas}")
        return create_response(
            success=True,
            data=[await meta.to_public_dict() for meta in user_metas],
            total=count,
        )

    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")


class UpdateUserMetaBody(BaseModel):
    status: Optional[bool] = None
    delete: Optional[bool] = None


@router.patch("/user-meta/{uuid}")
async def patch_user_meta(
    uuid: str, body: UpdateUserMetaBody, user_claims: UserClaims = Depends(require_auth)
):
    try:
        user_meta = await UserMeta.find_one(
            UserMeta.uuid == UUID(uuid),
            UserMeta.user.id == user_claims.user.id,  # type:ignore
        )
        if user_meta is None:
            raise Exception("Failed to find User Meta")
        user_meta.status = body.status if body.status is not None else user_meta.status

        if body.delete:
            user_meta.deleted_at = datetime.utcnow()
            user_meta.deleted_by = user_claims.user  # type:ignore

        await user_meta.save()

        return create_response(success=True, data=await user_meta.to_public_dict())

    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")
