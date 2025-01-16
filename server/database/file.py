from typing import List
from database.base import BaseMongoModel


class File(BaseMongoModel):
    file_name: str
    key: str
    file_type: str
    tags: List[str] = []
    status: bool = True
