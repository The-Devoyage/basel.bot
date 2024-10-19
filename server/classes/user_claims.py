from pydantic import BaseModel


class UserClaims(BaseModel):
    exp: int
    user_uuid: str
    auth_id: str
