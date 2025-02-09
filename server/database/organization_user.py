from beanie import Link
from database.base import BaseMongoModel
from database.user import User


class OrganizationUser(BaseMongoModel):
    user: Link[User]
    organization: Link["Organization"]  # type:ignore
    status: bool = True
