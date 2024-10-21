from pydantic import BaseModel


class UserClaims(BaseModel):
    exp: int
    user_uuid: str
    auth_id: str
    token_session_uuid: str
