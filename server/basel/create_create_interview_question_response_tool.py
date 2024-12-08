import logging
from llama_index.core.bridge.pydantic import Field
from llama_index.core.tools.function_tool import FunctionTool
from database.interview_question import InterviewQuestion
from database.interview_question_response import InterviewQuestionResponse

from database.user import User


logger = logging.getLogger(__name__)


async def create_interview_question_response(
    user: User,
    interview_question_uuid: str = Field(
        description="The UUID of the interview question being answered. Use the `get_interview_questions` tool to get the uuid, if needed."
    ),
    response: str = Field(
        description="A summary of the response when the user has finished conversation concerning answering the interview question."
    ),
):
    interview_question = await InterviewQuestion.find_one(
        InterviewQuestion.uuid == interview_question_uuid
    )
    interview_question_response = await InterviewQuestionResponse(
        user=user,  # type:ignore
        interview_question=interview_question,  # type:ignore
        response=response,
    ).create()
    # Handle Errors
    if not interview_question_response:
        raise Exception("Failed to create interview question response.")
    return interview_question_response.to_public_dict()


def create_create_interview_question_response_tool(user: User):
    create_interview_question_response_tool = FunctionTool.from_defaults(
        async_fn=lambda response, interview_question_uuid: create_interview_question_response(
            user, interview_question_uuid, response
        ),
        name="create_interview_question_response_tool",
        description="""
            Useful to log how a user responds to particular questions when taking an interview.
            """,
    )

    return create_interview_question_response_tool
