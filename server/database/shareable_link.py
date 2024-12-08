from typing import Optional
from datetime import datetime
from beanie import Document
from database.base import BaseMongoModel

from utils.environment import get_env_var

CLIENT_URL = get_env_var("CLIENT_URL")


class ShareableLink(BaseMongoModel):
    tag: Optional[str] = None
    token: Optional[str] = None
    status: bool = True

    def to_public_dict(self) -> dict:
        link = CLIENT_URL + f"?sl_token={self.token}"

        shareable_link = self.model_dump(exclude={"_id", "token"})

        shareable_link["link"] = link

        return shareable_link
