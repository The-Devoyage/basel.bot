import logging
from typing import List, Optional
from llama_index.core.bridge.pydantic import BaseModel, Field
from llama_index.core.tools.function_tool import FunctionTool

from database.interview import Interview, InterviewType
from database.user import User


logger = logging.getLogger(__name__)


class CreateInterviewParams(BaseModel):
    name: str = Field(description="The name of the interview.")
    description: str = Field(description="The description of the interview.")
    url: str = Field(
        description="The URL of the job posting associated with the interview you are creating."
    )
    organization_name: Optional[str] = Field(
        description="The organization or company name of which the interview belongs to."
    )
    interview_type: InterviewType = Field(
        description="The type of interview being created. Default to `general`."
    )
    position: Optional[str] = Field(
        description="The position associated with the application or interview."
    )
    tags: List[str] = Field(
        description="Tags, categories, and descriptors of the organziation, position, and interview."
    )


async def create_interview(
    current_user: User,
    name,
    description,
    url,
    organization_name,
    interview_type,
    position,
    tags,
):
    interview = await Interview(
        name=name,
        description=description,
        created_by=current_user,  # type:ignore
        organization_name=organization_name,
        url=url,
        interview_type=interview_type,
        position=position,
        tags=tags,
    ).create()
    if not interview:
        raise Exception("Failed to create interview.")
    return await interview.to_public_dict()


def create_create_interview_tool(current_user: User):
    create_interview_tool = FunctionTool.from_defaults(
        async_fn=lambda name, description, url, organization_name, interview_type, position, tags: create_interview(
            current_user,
            name,
            description,
            url,
            organization_name,
            interview_type,
            position,
            tags,
        ),
        name="create_interiew_tool",
        description="""
        Useful to create an interview object by the request of a user. 
        Once created interview questions may be created and associated with the interview.
        Always confirm before creating.
        """,
        fn_schema=CreateInterviewParams,
    )

    return create_interview_tool
