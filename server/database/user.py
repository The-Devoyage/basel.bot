import logging
from typing import Optional, Set
from uuid import UUID, uuid4
from beanie import Link
from llama_index.core.bridge.pydantic import Field
from database.base import BaseMongoModel
from database.role import Role

logger = logging.getLogger(__name__)


class User(BaseMongoModel):
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    role: Link[Role]
    status: bool = False
    auth_id: UUID = Field(default_factory=uuid4)

    exclude_from_public_dict: Set[str] = {"id", "auth_id"}
