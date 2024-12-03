from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class InterviewQuestionResponse(BaseModel):
    id: int
    uuid: str
    user_id: int
    interview_question_id: int
    response: str
    status: bool
    created_by: Optional[int]
    updated_by: Optional[int]
    deleted_by: Optional[int]
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    def to_public_dict(self) -> dict:
        interview_question_response = self.model_dump(
            exclude={"id", "created_by", "updated_by", "deleted_by"}
        )
        return interview_question_response
