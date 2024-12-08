from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from beanie import (
    Document,
    Insert,
    Link,
    TimeSeriesConfig,
    before_event,
)
from pydantic import Field


class BaseMongoModel(Document):
    uuid: UUID = Field(default_factory=uuid4)
    created_by: Optional[Link["User"]] = None  # type:ignore
    updated_by: Optional[Link["User"]] = None  # type:ignore
    deleted_by: Optional[Link["User"]] = None  # type:ignore
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None

    class Settings:
        timeseries = TimeSeriesConfig(
            time_field="created_at",  #  Required
        )

    @before_event(Insert)
    def update_updated_at(self):
        self.updated_at = datetime.now()

    def to_public_dict(self) -> dict:
        return self.model_dump(exclude={"_id"})
