import logging
from typing import List, Optional
from uuid import UUID
from llama_index.core.bridge.pydantic import BaseModel, Field
from llama_index.core.tools.function_tool import FunctionTool

from database.interview import Interview, InterviewType
from database.organization import Organization
from database.user import User


logger = logging.getLogger(__name__)


class CreateInterviewParams(BaseModel):
    name: str = Field(description="The name of the interview.")
    description: str = Field(description="The description of the interview.")
    url: Optional[str] = Field(
        description="The URL of the job posting associated with the interview you are creating.",
        default=None,
    )
    organization_uuid: Optional[str] = Field(
        description="The organization UUID, if provided, of which the interview belongs.",
        default=None,
    )
    interview_type: InterviewType = Field(
        description="The type of interview being created. Default to `general`.",
        default=None,
    )
    position: Optional[str] = Field(
        description="The position associated with the application or interview.",
        default=None,
    )
    tags: List[str] = Field(
        description="Tags, categories, and descriptors of the organziation, position, and interview.",
        default=[],
    )


async def create_interview(
    current_user: User,
    name: str,
    description: str,
    url: Optional[str] = None,
    organization_uuid: Optional[str] = None,
    interview_type: InterviewType = InterviewType.GENERAL,
    position: Optional[str] = None,
    tags: List[str] = [],
):
    try:
        organization = None
        if organization_uuid:
            organization = await Organization.find_one(
                Organization.uuid == UUID(organization_uuid)
            )

        interview = await Interview(
            name=name,
            description=description,
            created_by=current_user,  # type:ignore
            organization=organization,  # type:ignore
            url=url,
            interview_type=interview_type,
            position=position,
            tags=tags,
        ).create()
        if not interview:
            raise Exception("Failed to create interview.")
        return await interview.to_public_dict()
    except Exception as e:
        logger.error(e)
        return e


def create_create_interview_tool(current_user: User):
    create_interview_tool = FunctionTool.from_defaults(
        async_fn=lambda name, description, url=None, organization_uuid=None, interview_type=InterviewType.GENERAL, position=None, tags=[]: create_interview(
            current_user=current_user,
            name=name,
            description=description,
            url=url,
            organization_uuid=organization_uuid,
            interview_type=interview_type,
            position=position,
            tags=tags,
        ),
        name="create_interiew_tool",
        description="""
        Useful to insert an interview into the database by the request of a user. 
        Once created interview questions may be created and associated with the interview.
        Always confirm before creating.
        """,
        fn_schema=CreateInterviewParams,
    )

    return create_interview_tool
