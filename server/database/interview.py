from enum import Enum
from typing import List, Optional

from beanie import Indexed
from database.base import BaseMongoModel


class InterviewType(str, Enum):
    APPLICATION = "application"
    GENERAL = "general"


class Interview(BaseMongoModel):
    name: str
    description: str
    url: Indexed(str, unique=True) = None  # type:ignore
    organization_name: Optional[str] = None
    interview_type: InterviewType = InterviewType.GENERAL
    position: Optional[str] = None
    tags: List[str] = []
    status: bool = True
