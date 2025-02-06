from chromadb.api.models.Collection import Optional, logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from classes.user_claims import UserClaims
from database.organization_user import OrganizationUser
from utils.responses import create_response
from database.organization import Organization
from utils.jwt import optional_auth, require_auth
from database.file import File
from beanie.operators import In


router = APIRouter()

logger = logging.getLogger(__name__)


class CreateOrganizationParams(BaseModel):
    name: str
    description: str
    logo: Optional[File] = None


@router.post("/create")
async def create_organization(
    params: CreateOrganizationParams, user_claims: UserClaims = Depends(require_auth)
):
    organization = None
    try:
        organization = Organization(
            name=params.name,
            description=params.description,
            created_by=user_claims.user,  # type:ignore
        )

        if params.logo:
            file = await File.find_one(File.uuid == params.logo.uuid)
            if file:
                organization.logo = file  # type:ignore

        await organization.create()

        organization_member = OrganizationUser(
            user=user_claims.user,  # type:ignore
            organization=organization,  # type:ignore
            created_by=user_claims.user,  # type:ignore
        )

        await organization_member.create()

        return create_response(success=True, data=await organization.to_public_dict())
    except Exception as e:
        logger.error(e)
        if organization:
            await organization.delete()
        return HTTPException(status_code=500, detail="Something went wrong...")


@router.get("/list")
async def list_organizations(
    my_organizations: Optional[bool] = False,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    user_claims: Optional[UserClaims] = Depends(optional_auth),
):
    try:
        query = Organization.find(fetch_links=True)

        if my_organizations:
            if not user_claims:
                raise Exception("You must be logged in to search your organizations.")
            organization_users = await OrganizationUser.find(
                OrganizationUser.user.id == user_claims.user.id,  # type:ignore
                fetch_links=True,
            ).to_list()
            query.find(
                In(
                    Organization.id,
                    [
                        organization_user.organization.id  # type:ignore
                        for organization_user in organization_users
                    ],
                ),
                fetch_links=True,
            )

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
