from beanie import Link

from database.base import BaseMongoModel
from database.interview import Interview
from database.message import SenderIdentifer
from database.user import User


class InterviewTranscript(BaseMongoModel):
    interview: Link[Interview]
    user: Link[User]
    transcript: str
    sender: SenderIdentifer
    status: bool = True
