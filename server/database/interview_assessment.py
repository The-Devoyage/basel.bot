from beanie import Link
from database.base import BaseMongoModel
from typing import Optional
from database.interview import Interview

from database.user import User


class InterviewAssessment(BaseMongoModel):
    user: Link[User]
    interview: Link[Interview]
    overall: int
    content_relevance: Optional[int] = None
    communication_skills: Optional[int] = None
    confidence_delivery: Optional[int] = None
    structure_organization: Optional[int] = None
    adaptability_critical_thinking: Optional[int] = None
    technical_industry_knowledge: Optional[int] = None

    class Settings:
        max_nesting_depth = 4
