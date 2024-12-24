import logging
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Set
from uuid import UUID, uuid4
from beanie import (
    Document,
    Link,
    Save,
    Update,
    before_event,
)
from pydantic import Field

logger = logging.getLogger(__name__)


class BaseMongoModel(Document):
    uuid: UUID = Field(default_factory=uuid4)
    created_by: Optional[Link["User"]] = None  # type:ignore
    updated_by: Optional[Link["User"]] = None  # type:ignore
    deleted_by: Optional[Link["User"]] = None  # type:ignore
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = None

    @before_event(Save, Update)
    def update_updated_at(self):
        self.updated_at = datetime.now(timezone.utc)

    def exclude_from_public_dict(self) -> Set[str]:
        return {"id"}

    def get_virtual_fields(self) -> Dict[str, Any]:
        """
        Override this method in child classes to define virtual fields.
        """
        return {}

    async def to_public_dict(self, exclude: Optional[Set[str]] = None) -> dict:
        # Combine class-level and method-level excludes
        exclude = exclude or set()
        exclude = exclude.union(self.exclude_from_public_dict())

        # Serialize the model and exclude specified fields
        public_dict = self.model_dump(exclude=exclude)

        # Add virtual fields
        virtual_fields = self.get_virtual_fields()
        public_dict.update(virtual_fields)

        # Convert linked objects recursively
        for key, value in self:
            if hasattr(value, "to_public_dict"):
                public_dict[key] = await value.to_public_dict()  # type:ignore
            elif isinstance(value, Link):
                public_dict[key] = None

        return public_dict

    class Settings:
        name = None
