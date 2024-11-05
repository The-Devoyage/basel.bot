from pydantic import BaseModel

from classes.user import User


class UserClaims(BaseModel):
    exp: int
    user_uuid: str
    auth_id: str
    token_session_uuid: str
    user: User


class ShareableLinkClaims(BaseModel):
    user_uuid: str
    shareable_link_uuid: str
