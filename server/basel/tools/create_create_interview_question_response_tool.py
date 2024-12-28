from uuid import UUID
from llama_index.core.bridge.pydantic import BaseModel, Field
from llama_index.core.tools.function_tool import FunctionTool
from database.interview_question import InterviewQuestion
from database.interview_question_response import InterviewQuestionResponse

from database.user import User


class CreateInterviewQuestionResponseParams(BaseModel):
    interview_question_uuid: str = Field(
        description="The UUID of the interview question being answered. Use the `get_interview_questions` tool to get the uuid, if needed."
    )
    response: str = Field(
        description="A summary of the response when the user has finished conversation concerning answering the interview question."
    )


async def create_interview_question_response(
    user: User, interview_question_uuid, response
):
    interview_question = await InterviewQuestion.find_one(
        InterviewQuestion.uuid == UUID(interview_question_uuid)
    )

    if not interview_question:
        raise Exception("Interview question not found.")

    interview_question_response = await InterviewQuestionResponse(
        user=user,  # type:ignore
        interview_question=interview_question,  # type:ignore
        response=response,
        created_by=user,  # type:ignore
    ).create()

    # Handle Errors
    if not interview_question_response:
        raise Exception("Failed to create interview question response.")

    return await interview_question_response.to_public_dict()


def create_create_interview_question_response_tool(user: User):
    create_interview_question_response_tool = FunctionTool.from_defaults(
        async_fn=lambda response, interview_question_uuid: create_interview_question_response(
            user, interview_question_uuid, response
        ),
        name="create_interview_question_response_tool",
        description="""
            Useful for saving user responses to interview questions.
            """,
        fn_schema=CreateInterviewQuestionResponseParams,
    )

    return create_interview_question_response_tool
