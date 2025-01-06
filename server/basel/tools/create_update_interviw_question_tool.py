from typing import Optional
from uuid import UUID
from llama_index.core.bridge.pydantic import BaseModel, Field
from llama_index.core.tools.function_tool import FunctionTool
from llama_index.readers.web.async_web.base import logging

from database.interview_question import InterviewQuestion
from database.role import Role, RoleIdentifier
from database.user import User

logger = logging.getLogger(__name__)


class UpdateInterviewQuestionParams(BaseModel):
    interview_question_uuid: str = Field(
        description="The UUID of the `interview question` to update."
    )
    question: Optional[str] = Field(description="Optional string of updated question.")
    status: Optional[bool] = Field(
        description="Optional boolean to alter the status of the question. Inactive questions are not part of interviews."
    )


async def update_interview_question(
    user: User, interview_question_uuid: str, question, status, role: Role
):
    try:
        if role.identifier == RoleIdentifier.ADMIN:  # type:ignore
            interview_question = await InterviewQuestion.find_one(
                InterviewQuestion.uuid == UUID(interview_question_uuid)
            )
        else:
            interview_question = await InterviewQuestion.find_one(
                InterviewQuestion.uuid == UUID(interview_question_uuid),
                InterviewQuestion.created_by.id == user.id,  # type:ignore
            )

        if interview_question is None:
            return "Interview question not found."

        interview_question.updated_by = user  # type:ignore

        if question is not None:
            interview_question.question = question

        if status is not None:
            interview_question.status = status

        await interview_question.save()

        return interview_question

    except Exception as e:
        logger.error(e)
        return "Something went wrong.."


def create_update_interview_question_tool(current_user: User, role: Role):
    update_interview_question_tool = FunctionTool.from_defaults(
        name="update_interview_question_tool",
        description="Useful to update a question or status of a question associated with an interview but not the interview itself.",
        async_fn=lambda interview_question_uuid, question, status: update_interview_question(
            user=current_user,
            role=role,
            interview_question_uuid=interview_question_uuid,
            status=status,
            question=question,
        ),
        fn_schema=UpdateInterviewQuestionParams,
    )
    return update_interview_question_tool
