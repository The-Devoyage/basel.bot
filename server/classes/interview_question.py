from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class InterviewQuestion(BaseModel):
    id: int
    uuid: str
    interview_id: int
    question: str
    status: bool
    created_by: Optional[int]
    updated_by: Optional[int]
    deleted_by: Optional[int]
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    def to_public_dict(self) -> dict:
        interview_question = self.model_dump(
            exclude={"id", "created_by", "updated_by", "deleted_by"}
        )
        return interview_question
