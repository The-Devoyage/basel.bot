import logging
from typing import Optional
from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends
from classes.user_claims import UserClaims
from database.shareable_link import ShareableLinkModel
from utils.environment import get_env_var
from pydantic import BaseModel

from utils.jwt import create_jwt, require_auth
from utils.responses import create_response

router = APIRouter()

logger = logging.getLogger(__name__)

# Database
shareable_link_model = ShareableLinkModel("basel.db")

# Constants
SHAREABLE_LINK_SECRET = get_env_var("SHAREABLE_LINK_SECRET")


class CreateShareableLinkBody(BaseModel):
    tag: str


@router.post("/shareable-link")
async def create_shareable_link(
    body: CreateShareableLinkBody, user_claims: UserClaims = Depends(require_auth)
):
    try:
        conn = shareable_link_model._get_connection()
        cursor = conn.cursor()

        # Create Shareable Link
        updated = shareable_link_model.create_shareable_link(
            cursor, user_claims.user.id, body.tag
        )

        conn.commit()

        if updated is None:
            raise Exception("Failed to create Shareable Link")

        shareable_link = shareable_link_model.get_shareable_link_by_id(cursor, updated)

        if shareable_link is None:
            raise Exception("Failed to find Shareable Link")

        # Create the Token with Payload
        payload = {
            "user_uuid": user_claims.user_uuid,
            "shareable_link_uuid": shareable_link.uuid,
        }

        token = create_jwt(payload, SHAREABLE_LINK_SECRET)

        # Save The Token
        updated = shareable_link_model.update_shareable_link(
            cursor,
            shareable_link_id=updated,
            token=token,
            current_user=user_claims.user,
        )

        if updated == 0:
            raise Exception("Unable to update sharebale link")

        # Commit
        conn.commit()

        shareable_link = shareable_link_model.get_shareable_link_by_id(
            cursor, shareable_link.id
        )

        conn.close()

        if not shareable_link:
            raise Exception("Shareable link not found")

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
    user_claims: UserClaims = Depends(require_auth),
):
    try:
        conn = shareable_link_model._get_connection()
        cursor = conn.cursor()
        shareable_link = shareable_link_model.get_shareable_link_by_uuid(cursor, uuid)

        if shareable_link is None:
            raise Exception("Failed to find shareable link.")

        update_count = shareable_link_model.update_shareable_link(
            cursor,
            shareable_link_id=shareable_link.id,
            status=body.status,
            tag=body.tag,
            current_user=user_claims.user,
        )

        if not update_count:
            raise Exception("Failed to update shareable link")

        conn.commit()

        shareable_link = shareable_link_model.get_shareable_link_by_id(
            cursor, shareable_link.id
        )

        if not shareable_link:
            raise Exception("Shareable link not found")

        return create_response(success=True, data=shareable_link.to_public_dict())
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")


@router.get("/shareable-link")
async def get_shareable_link(id: int, _: UserClaims = Depends(require_auth)):
    try:
        conn = shareable_link_model._get_connection()
        cursor = conn.cursor()
        shareable_link = shareable_link_model.get_shareable_link_by_id(cursor, id)

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
        conn = shareable_link_model._get_connection()
        cursor = conn.cursor()
        shareable_links = shareable_link_model.get_shareable_links(
            cursor, user_claims.user.id, limit, offset
        )

        return create_response(
            success=True, data=[link.to_public_dict() for link in shareable_links]
        )
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")
