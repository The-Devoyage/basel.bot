from beanie import Link

from database.base import BaseMongoModel
from database.interview import Interview
from database.user import User


class InterviewTranscript(BaseMongoModel):
    interview: Link[Interview]
    user: Link[User]
    transcript: str
    status: bool = True
