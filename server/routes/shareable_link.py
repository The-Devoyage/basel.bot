import logging
from uuid import UUID
import jwt
from typing import List, Optional, cast
from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends
from classes.user_claims import ShareableLinkClaims, UserClaims
from database.interview import Interview
from database.shareable_link import ShareableLink
from utils.environment import get_env_var
from pydantic import BaseModel
from beanie.operators import In

from utils.jwt import create_jwt, require_auth
from utils.responses import create_response

router = APIRouter()

logger = logging.getLogger(__name__)

# Constants
SHAREABLE_LINK_SECRET = get_env_var("SHAREABLE_LINK_SECRET")
ALGORITHM = get_env_var("JWT_ALGORITHM")


@router.post("/shareable-link")
async def create_shareable_link(user_claims: UserClaims = Depends(require_auth)):
    try:
        shareable_link = await ShareableLink(
            created_by=user_claims.user,  # type:ignore
            updated_by=user_claims.user,  # type:ignore
            user=user_claims.user,  # type:ignore
        ).create()

        if shareable_link is None:
            raise Exception("Failed to create Shareable Link")

        # Create the Token with Payload
        payload = {
            "user_uuid": user_claims.user_uuid,
            "shareable_link_uuid": str(shareable_link.uuid),
        }

        token = create_jwt(payload, SHAREABLE_LINK_SECRET)

        shareable_link.token = token

        await shareable_link.save()

        if not shareable_link:
            raise Exception("Unable to create link token.")

        return create_response(success=True, data=await shareable_link.to_public_dict())

    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")


class UpdateShareableLinkBody(BaseModel):
    status: Optional[bool] = None
    tag: Optional[str] = None
    interview_uuids: Optional[List[str]] = None


@router.patch("/shareable-link/{uuid}")
async def update_shareable_link(
    uuid: str,
    body: UpdateShareableLinkBody,
    user_claims: UserClaims = Depends(require_auth),
):
    try:
        shareable_link = await ShareableLink.find_one(
            ShareableLink.uuid == UUID(uuid),
            ShareableLink.user.id == user_claims.user.id,  # type:ignore
        )

        if shareable_link is None:
            raise Exception("Failed to find shareable link.")

        shareable_link.status = (
            body.status if body.status is not None else shareable_link.status
        )
        shareable_link.tag = body.tag if body.tag is not None else shareable_link.tag
        shareable_link.updated_by = user_claims.user  # type:ignore

        if body.interview_uuids:
            interviews = await Interview.find(
                In(Interview.uuid, [UUID(uuid) for uuid in body.interview_uuids])
            ).to_list()
            shareable_link.interviews = interviews  # type:ignore
        else:
            shareable_link.interviews = None

        await shareable_link.save()

        if not shareable_link:
            raise Exception("Failed to update shareable link")

        return create_response(success=True, data=await shareable_link.to_public_dict())
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")


@router.get("/shareable-link/{sl_token}")
async def get_shareable_link(sl_token: str):
    try:
        decoded = jwt.decode(sl_token, SHAREABLE_LINK_SECRET, algorithms=[ALGORITHM])
        sl_claims = cast(ShareableLinkClaims, ShareableLinkClaims(**decoded))
        shareable_link = await ShareableLink.find_one(
            ShareableLink.uuid == UUID(sl_claims.shareable_link_uuid), fetch_links=True
        )
        if not shareable_link:
            raise Exception("Shareable link not found")

        return create_response(success=True, data=await shareable_link.to_public_dict())
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")


@router.get("/shareable-links")
async def get_shareable_links(
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    interview_uuid: Optional[UUID] = None,
    user_claims: UserClaims = Depends(require_auth),
):
    try:
        query = ShareableLink.find(
            ShareableLink.user.id == user_claims.user.id,  # type:ignore
            fetch_links=True,
        )

        if interview_uuid:
            query.find(
                ShareableLink.interviews.uuid == interview_uuid, fetch_links=True
            )

        shareable_links = await query.limit(limit).skip(offset).to_list()
        logger.debug(f"SHAREABLE LINKS: {shareable_links}")
        return create_response(
            success=True, data=[await link.to_public_dict() for link in shareable_links]
        )
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")
