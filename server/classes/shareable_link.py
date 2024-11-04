from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from utils.environment import get_env_var

CLIENT_URL = get_env_var("CLIENT_URL")


class ShareableLink(BaseModel):
    id: int
    uuid: str
    tag: Optional[str]
    token: str
    status: bool
    created_by: Optional[int]
    updated_by: Optional[int]
    deleted_by: Optional[int]
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    def to_public_dict(self) -> dict:
        link = CLIENT_URL + f"token={self.token}"

        shareable_link = self.model_dump(
            exclude={"id", "created_by", "updated_by", "deleted_by", "token"}
        )

        shareable_link["link"] = link

        return shareable_link
