from typing import Optional
from database.base import BaseMongoModel

from utils.environment import get_env_var

CLIENT_URL = get_env_var("CLIENT_URL")


class ShareableLink(BaseMongoModel):
    tag: Optional[str] = None
    token: Optional[str] = None
    status: bool = True

    def get_virtual_fields(self) -> dict:
        """
        Add virtual fields to the serialized output.
        """
        return {"link": f"{CLIENT_URL}?sl_token={self.token}" if self.token else None}
