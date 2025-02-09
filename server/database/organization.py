from typing import List, Set

from beanie import BackLink, Link
from chromadb.api.models.Collection import Optional
from pydantic import Field
from database.base import BaseMongoModel
from database.organization_user import OrganizationUser
from database.file import File


class Organization(BaseMongoModel):
    name: str
    description: str
    status: bool = True
    logo: Optional[Link[File]] = None
    users: List[BackLink[OrganizationUser]] = Field(
        original_field="organization"  # type:ignore
    )
    slug: str

    def exclude_from_public_dict(self) -> Set[str]:
        return {"id"}
