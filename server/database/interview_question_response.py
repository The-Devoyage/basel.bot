from beanie import Link

from database.base import BaseMongoModel
from database.interview_question import InterviewQuestion
from database.user import User


class InterviewQuestionResponse(BaseMongoModel):
    user: Link[User]
    interview_question: Link[InterviewQuestion]
    response: str
    status: bool = True
