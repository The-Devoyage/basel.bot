from beanie import Link

from database.base import BaseMongoModel
from database.interview import Interview


class InterviewQuestion(BaseMongoModel):
    interview: Link[Interview]
    question: str
    status: bool = True
