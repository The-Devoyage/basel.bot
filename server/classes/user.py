from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    id: int
    uuid: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    role_id: int
    status: bool
    file: Optional[int]
    auth_id: str
    created_by: Optional[int]
    updated_by: Optional[int]
    deleted_by: Optional[int]
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]
