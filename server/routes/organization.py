from chromadb.api.models.Collection import Optional, logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from classes.user_claims import UserClaims
from utils.responses import create_response
from database.organization import Organization
from utils.jwt import optional_auth, require_auth


router = APIRouter()

logger = logging.getLogger(__name__)


class CreateOrganizationParams(BaseModel):
    name: str
    description: str


@router.post("/")
async def create_organization(
    params: CreateOrganizationParams, user_claims: UserClaims = Depends(require_auth)
):
    try:
        organization = await Organization(
            name=params.name,
            description=params.description,
            created_by=user_claims.user,  # type:ignore
        ).create()

        return create_response(success=True, data=await organization.to_public_dict())
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")


@router.get("/list")
async def list_organizations(
    my_organizations: Optional[bool] = False,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    user_claims: Optional[UserClaims] = Depends(optional_auth),
):
    try:
        query = Organization.find()

        if my_organizations:
            if not user_claims:
                raise Exception("You must be logged in to search your organizations.")
            query.find(Organization.organization_members == user_claims.user.id)

        organizations = await query.limit(limit).skip(offset).to_list()

        return create_response(
            success=True,
            data=[
                await organization.to_public_dict() for organization in organizations
            ],
        )

    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail=str(e))
