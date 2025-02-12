import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set
from uuid import UUID, uuid4
from beanie import (
    BackLink,
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

    async def to_public_dict(
        self,
        exclude: Optional[Set[str]] = None,
        json: bool = False,
    ) -> dict:
        # Combine class-level and method-level excludes
        exclude = exclude if exclude else self.exclude_from_public_dict()

        # Serialize the model and exclude specified fields
        public_dict = self.model_dump(exclude=exclude)

        # Add virtual fields
        virtual_fields = self.get_virtual_fields()
        public_dict.update(virtual_fields)

        # Convert linked objects recursively
        for key, value in self:
            if key in exclude:
                continue

            # Make UUIDs JSON Serializable
            if key == "uuid" and json:
                public_dict["uuid"] = str(value)

            # Make datetimes JSON Serializable
            if isinstance(value, datetime):
                public_dict[key] = str(value)

            # Recursively Replace
            if hasattr(value, "to_public_dict"):
                public_dict[key] = await value.to_public_dict(json=json)  # type:ignore
            elif isinstance(value, List):
                if all(hasattr(v, "to_public_dict") for v in value):
                    public_dict[key] = [
                        await v.to_public_dict(json=json) for v in value
                    ]
                elif isinstance(value, Link) or isinstance(value, BackLink):
                    public_dict[key] = None
                elif any(isinstance(v, BackLink) for v in value):
                    public_dict[key] = None
                else:
                    public_dict[key] = value  # Leave as-is if not all are serializable
            elif isinstance(value, Link) or isinstance(value, BackLink):
                public_dict[key] = None

        return public_dict

    class Settings:
        name = None
