from pydantic import BaseModel


class TokenSession(BaseModel):
    id: int
    user_id: str
    uuid: str
    status: bool
    created_at: str
