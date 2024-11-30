import logging
from llama_index.core.bridge.pydantic import Field
from llama_index.core.tools.function_tool import FunctionTool
from classes.interview import Interview

from database.interview import InterviewModel

interview_model = InterviewModel("basel.db")

logger = logging.getLogger(__name__)


def create_interview(
    current_user_id: int,
    name: str = Field(description="The name of the interview."),
    description: str = Field(description="The description of the interview."),
) -> Interview:
    conn = interview_model._get_connection()
    cursor = conn.cursor()
    interview_id = interview_model.create_interview(
        cursor, current_user_id, name, description
    )
    if not interview_id:
        raise Exception("Failed to create interview.")
    interview = interview_model.get_interview_by_id(cursor, interview_id)
    if not interview:
        raise Exception("Failed to find interview.")
    conn.commit()
    conn.close()
    return interview


def create_create_interview_tool(current_user_id: int):
    create_interview_tool = FunctionTool.from_defaults(
        fn=lambda name, description: create_interview(
            current_user_id, name, description
        ),
        name="create_interiew_tool",
        description="""
        Useful to create an interview object by the request of a user. 
        Once created interview questions may be created and associated with the interview.
        Always confirm before creating.
        """,
    )

    return create_interview_tool
