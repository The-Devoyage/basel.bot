from beanie import Link
from chromadb.api.models.Collection import Optional
from database.base import BaseMongoModel
from database.file import File


class Organization(BaseMongoModel):
    name: str
    description: str
    status: bool = True
    logo: Optional[Link[File]] = None
