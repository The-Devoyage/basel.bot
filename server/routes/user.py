from typing import Optional
from uuid import UUID
from boto3 import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from database.file import File
from classes.user_claims import UserClaims
from database.user import User
from utils.jwt import require_auth
from utils.responses import create_response

logger = logging.getLogger(__name__)

router = APIRouter()


class UpdateUserParams(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    profile_image: Optional[UUID] = None


@router.patch("/update")
async def update_user(
    params: UpdateUserParams, user_claims: UserClaims = Depends(require_auth)
):
    try:
        user = await User.find_one(User.id == user_claims.user.id)

        if not user:
            return HTTPException(status_code=500, detail="Failed to find user.")

        if params.first_name:
            user.first_name = params.first_name
        if params.last_name:
            user.last_name = params.last_name
        if params.profile_image:
            profile_image = await File.find_one(
                File.uuid == params.profile_image,
                File.created_by.id == user_claims.user.id,  # type:ignore
            )
            if not profile_image:
                return HTTPException(
                    status_code=500, detail="Failed to find profile image."
                )
            user.profile_image = profile_image  # type:ignore
        await user.save()

        return create_response(success=True, data=await user.to_public_dict())

    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")
