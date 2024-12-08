import logging
from llama_index.core.bridge.pydantic import Field
from llama_index.core.tools.function_tool import FunctionTool

from database.interview import Interview
from database.user import User


logger = logging.getLogger(__name__)


async def create_interview(
    current_user: User,
    name: str = Field(description="The name of the interview."),
    description: str = Field(description="The description of the interview."),
):
    interview = await Interview(
        name=name, description=description, created_by=current_user  # type:ignore
    ).create()
    if not interview:
        raise Exception("Failed to create interview.")
    return interview.to_public_dict()


def create_create_interview_tool(current_user: User):
    create_interview_tool = FunctionTool.from_defaults(
        async_fn=lambda name, description: create_interview(
            current_user, name, description
        ),
        name="create_interiew_tool",
        description="""
        Useful to create an interview object by the request of a user. 
        Once created interview questions may be created and associated with the interview.
        Always confirm before creating.
        """,
    )

    return create_interview_tool
