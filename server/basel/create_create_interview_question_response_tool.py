import logging
from llama_index.core.bridge.pydantic import Field
from llama_index.core.tools.function_tool import FunctionTool

from database.interview_question_response import InterviewQuestionResponseModel

interview_question_response_model = InterviewQuestionResponseModel("basel.db")

logger = logging.getLogger(__name__)


def create_interview_question_response(
    user_id: int,
    interview_question_uuid: str = Field(
        description="The UUID of the interview question being answered. Use the `get_interview_questions` tool to get the uuid, if needed."
    ),
    response: str = Field(
        description="A summary of the response when the user has finished conversation concerning answering the interview question."
    ),
):
    conn = interview_question_response_model._get_connection()
    cursor = conn.cursor()
    interview_question_response_id = (
        interview_question_response_model.create_interview_question_response(
            cursor, user_id, interview_question_uuid, response
        )
    )
    conn.commit()
    # Handle Errors
    if not interview_question_response_id:
        conn.close()
        raise Exception("Failed to create interview question response.")
    interview_question_response = (
        interview_question_response_model.get_interview_question_response_by_id(
            cursor, interview_question_response_id
        )
    )
    conn.close()
    if not interview_question_response:
        conn.close()
        raise Exception("Failed to find interview question response.")
    return interview_question_response.to_public_dict()


def create_create_interview_question_response_tool(user_id: int):
    create_interview_question_response_tool = FunctionTool.from_defaults(
        fn=lambda response, interview_question_uuid: create_interview_question_response(
            user_id, interview_question_uuid, response
        ),
        name="create_interview_question_response_tool",
        description="""
            Useful to log how a user responds to particular questions when taking an interview.
            """,
    )

    return create_interview_question_response_tool
