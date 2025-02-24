from beanie import Link

from database.base import BaseMongoModel
from database.interview_question import InterviewQuestion


class InterviewQuestionResponse(BaseMongoModel):
    user: Link["User"]  # type:ignore
    interview_question: Link[InterviewQuestion]
    response: str
    status: bool = True
