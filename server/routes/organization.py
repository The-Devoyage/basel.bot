from beanie import SortDirection
from chromadb.api.models.Collection import Optional, logging
from chromadb.api.models.CollectionCommon import UUID
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from classes.user_claims import UserClaims
from database.organization_user import OrganizationUser
from utils.responses import create_response
from database.organization import Organization
from utils.jwt import optional_auth, require_auth
from database.file import File
from beanie.operators import In, ElemMatch


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
        existing_org = await Organization.find_one(Organization.name == params.name)
        if existing_org:
            return HTTPException(status_code=400, detail="Organization already exists.")

        organization = Organization(
            name=params.name,
            description=params.description,
            created_by=user_claims.user,  # type:ignore
            slug=params.name.replace(" ", "-").lower(),
        )

        if params.logo:
            file = await File.find_one(File.uuid == params.logo.uuid)
            if file:
                organization.logo = file  # type:ignore

        organization = await organization.create()

        organization_member = OrganizationUser(
            user=user_claims.user,  # type:ignore
            organization=organization,  # type:ignore
            created_by=user_claims.user,  # type:ignore
        )

        await organization_member.create()

        organization = await Organization.find_one(
            Organization.id == organization.id,
            fetch_links=True,
        )

        if not organization:
            return HTTPException(status_code=500, detail="Failed to find organization.")

        return create_response(success=True, data=await organization.to_public_dict())
    except Exception as e:
        logger.error(e)
        if organization:
            await organization.delete()
        return HTTPException(status_code=500, detail="Something went wrong...")


class UpdateOrganizationParams(BaseModel):
    uuid: UUID
    name: Optional[str] = None
    description: Optional[str] = None
    logo: Optional[File] = None


@router.patch("/update")
async def update_organization(
    params: UpdateOrganizationParams, user_claims: UserClaims = Depends(require_auth)
):
    try:
        if not params.name and not params.description and not params.logo:
            return HTTPException(status_code=400, detail="Missing update fields.")

        organization = await Organization.find_one(
            Organization.uuid == params.uuid,
        )

        if not organization:
            return HTTPException(status_code=400, detail="Organization not found.")

        if params.name and params.name != organization.name:
            exists = await Organization.find(Organization.name == params.name).exists()
            if exists:
                return HTTPException(
                    status_code=400, detail="Organization already exists."
                )
            organization.name = params.name
            organization.slug = params.name.replace(" ", "-").lower()
        if params.description:
            organization.description = params.description
        if params.logo:
            file = await File.find_one(File.uuid == params.logo.uuid)
            if file:
                organization.logo = file  # type:ignore

        organization.updated_by = user_claims.user  # type:ignore

        organization = await organization.save()

        organization = await Organization.find_one(
            Organization.id == organization.id,
            fetch_links=True,
        )

        if not organization:
            return HTTPException(status_code=500, detail="Failed to find organization.")

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
        query = Organization.find(
            fetch_links=True,
        )

        if my_organizations:
            if not user_claims:
                raise Exception("You must be logged in to search your organizations.")
            query.find(
                Organization.users.user._id == user_claims.user.id,  # type:ignore
                fetch_links=True,
            )

        total = await query.count()
        organizations = (
            await query.limit(limit)
            .skip(offset)
            .sort(
                [(Organization.created_at, SortDirection.DESCENDING)]  # type:ignore
            )
            .to_list()
        )

        return create_response(
            success=True,
            data=[
                await organization.to_public_dict() for organization in organizations
            ],
            total=total,
        )

    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def get_organizations(
    slug: str,
    _: Optional[UserClaims] = Depends(optional_auth),
):
    try:
        organization = await Organization.find_one(
            Organization.slug == slug.lower(),
            fetch_links=True,
        )

        logger.debug(f"HER HER {organization}")

        if not organization:
            return HTTPException(status_code=400, detail="Organization not found.")

        return create_response(success=True, data=await organization.to_public_dict())
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail=str(e))
