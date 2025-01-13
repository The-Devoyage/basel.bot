from typing import List
from database.base import BaseMongoModel


class File(BaseMongoModel):
    name: str
    description: str
    key: str
    extension: str
    tags: List[str] = []
    status: bool = True
