from typing import Optional
from uuid import UUID
from llama_index.core.bridge.pydantic import BaseModel, Field
from llama_index.core.tools.function_tool import FunctionTool
from llama_index.readers.web.async_web.base import logging

from database.interview_question import InterviewQuestion

logger = logging.getLogger(__name__)


class UpdateInterviewQuestionParams(BaseModel):
    interview_question_uuid: str = Field(
        description="The UUID of the `interview question` to update."
    )
    question: Optional[str] = Field(description="Optional string of updated question.")
    status: Optional[bool] = Field(
        description="Optional boolean to alter the status of the question. Inactive questions are not part of interviews."
    )


async def update_interview_question(interview_question_uuid: str, question, status):
    try:
        interview_question = await InterviewQuestion.find_one(
            InterviewQuestion.uuid == UUID(interview_question_uuid)
        )

        if interview_question is None:
            return "Interview question not found."

        if question is not None:
            interview_question.question = question

        if status is not None:
            interview_question.status = status

        await interview_question.save()

        return interview_question

    except Exception as e:
        logger.error(e)
        return "Something went wrong.."


def create_update_interview_question_tool():
    update_interview_question_tool = FunctionTool.from_defaults(
        name="update_interview_question_tool",
        description="Useful to update a question or status of a question associated with an interview but not the interview itself.",
        async_fn=update_interview_question,
        fn_schema=UpdateInterviewQuestionParams,
    )
    return update_interview_question_tool
