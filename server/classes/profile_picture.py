from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from utils.environment import get_env_var

CLIENT_URL = get_env_var("CLIENT_URL")

class ProfilePicture(BaseModel):
  id: int
  user_id: int
  filename: str
  file_extension: str
  file_path: str
  created_by: Optional[int]
  updated_by: Optional[int]
  deleted_by: Optional[int]
  created_at: datetime
  updated_at: datetime
  deleted_at: Optional[datetime]
  