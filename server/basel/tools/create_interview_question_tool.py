from uuid import UUID
from llama_index.core.bridge.pydantic import BaseModel, Field
from llama_index.core.tools.function_tool import FunctionTool
from database.interview import Interview
import logging
from database.interview_question import InterviewQuestion
from database.user import User

logger = logging.getLogger(__name__)


class CreateInterviewQuestionParams(BaseModel):
    interview_uuid: str = Field(
        description="The UUID of an interview to associate the question with."
    )
    question: str = Field(description="The question associated with an interview.")


async def create_interview_question(current_user: User, interview_uuid, question):
    try:
        interview = await Interview.find_one(
            Interview.uuid == UUID(interview_uuid),
            Interview.created_by.id == current_user.id,  # type:ignore
        )

        if not interview:
            raise Exception(
                "Interview not found or user does not have permission to add questions to interivews they did not create."
            )

        interview_question = await InterviewQuestion(
            interview=interview,  # type:ignore
            question=question,
            created_by=current_user,  # type:ignore
        ).create()

        if not interview_question:
            raise Exception("Failed to create interview question.")

        return await interview_question.to_public_dict()
    except Exception as e:
        logger.error(e)
        return e


def create_create_interview_question_tool(current_user: User):
    create_interview_question_tool = FunctionTool.from_defaults(
        async_fn=lambda interview_uuid, question: create_interview_question(
            current_user, interview_uuid, question
        ),
        name="create_interview_question_tool",
        description="""
        Useful for adding new questions to interviews.
        """,
        fn_schema=CreateInterviewQuestionParams,
    )
    return create_interview_question_tool
