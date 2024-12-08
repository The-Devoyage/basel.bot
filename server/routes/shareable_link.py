import logging
import jwt
from beanie.operators import Set
from typing import Optional, cast
from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends
from classes.user_claims import ShareableLinkClaims, UserClaims
from database.shareable_link import ShareableLink
from utils.environment import get_env_var
from pydantic import BaseModel

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
        shareable_link = await ShareableLink().create()

        if shareable_link is None:
            raise Exception("Failed to create Shareable Link")

        # Create the Token with Payload
        payload = {
            "user_uuid": user_claims.user_uuid,
            "shareable_link_uuid": shareable_link.uuid,
        }

        token = create_jwt(payload, SHAREABLE_LINK_SECRET)

        shareable_link = await shareable_link.update(Set({"token": token}))

        if not shareable_link:
            raise Exception("Unable to create link token.")

        return create_response(success=True, data=shareable_link.to_public_dict())

    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")


class UpdateShareableLinkBody(BaseModel):
    status: Optional[bool] = None
    tag: Optional[str] = None


@router.patch("/shareable-link/{uuid}")
async def update_shareable_link(
    uuid: str,
    body: UpdateShareableLinkBody,
    _: UserClaims = Depends(require_auth),
):
    try:
        shareable_link = await ShareableLink.find_one(ShareableLink.uuid == uuid)

        if shareable_link is None:
            raise Exception("Failed to find shareable link.")

        shareable_link = await shareable_link.update(
            Set({"status": body.status, "tag": body.tag})
        )

        if not shareable_link:
            raise Exception("Failed to update shareable link")

        return create_response(success=True, data=shareable_link.to_public_dict())
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")


@router.get("/shareable-link/{sl_token}")
async def get_shareable_link(sl_token: str):
    try:
        decoded = jwt.decode(sl_token, SHAREABLE_LINK_SECRET, algorithms=[ALGORITHM])
        sl_claims = cast(ShareableLinkClaims, ShareableLinkClaims(**decoded))
        shareable_link = await ShareableLink.find_one(
            ShareableLink.uuid == sl_claims.shareable_link_uuid
        )
        if not shareable_link:
            raise Exception("Shareable link not found")

        return create_response(success=True, data=shareable_link.to_public_dict())
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")


@router.get("/shareable-links")
async def get_shareable_links(
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    user_claims: UserClaims = Depends(require_auth),
):
    try:
        shareable_links = (
            await ShareableLink.find_many(ShareableLink.created_by == user_claims.user)
            .limit(limit)
            .skip(offset)
            .to_list()
        )
        return create_response(
            success=True, data=[link.to_public_dict() for link in shareable_links]
        )
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")
