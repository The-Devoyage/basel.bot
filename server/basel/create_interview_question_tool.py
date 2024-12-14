from uuid import UUID
from llama_index.core.bridge.pydantic import Field
from llama_index.core.tools.function_tool import FunctionTool
from database.interview import Interview

from database.interview_question import InterviewQuestion
from database.user import User


async def create_interview_question(
    current_user: User,
    interview_uuid: str = Field(
        description="The UUID of an interview to associate the question with."
    ),
    question: str = Field(description="The question associated with an interview."),
):
    interview = await Interview.find_one(Interview.uuid == UUID(interview_uuid))

    if not interview:
        raise Exception("Interview not found.")

    interview_question = await InterviewQuestion(
        interview=interview,  # type:ignore
        question=question,
        created_by=current_user,  # type:ignore
    ).create()

    if not interview_question:
        raise Exception("Failed to create interview question.")

    return await interview_question.to_public_dict()


def create_create_interview_question_tool(current_user: User):
    create_interview_question_tool = FunctionTool.from_defaults(
        async_fn=lambda interview_uuid, question: create_interview_question(
            current_user, interview_uuid, question
        ),
        name="create_interview_question_tool",
        description="Useful to create an associate a question to an intervview.",
    )
    return create_interview_question_tool
