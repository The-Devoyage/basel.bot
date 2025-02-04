from typing import List

from beanie import BackLink
from database.base import BaseMongoModel
from database.organization_user import OrganizationUser


class Organization(BaseMongoModel):
    name: str
    description: str
    status: bool = True
    organization_members: List[BackLink[OrganizationUser]]
