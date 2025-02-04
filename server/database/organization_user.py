from fastapi.openapi.models import Link
from database.base import BaseMongoModel
from database.organization import Organization
from database.user import User


class OrganizationUser(BaseMongoModel):
    user: Link[User]
    organization: Link[Organization]
