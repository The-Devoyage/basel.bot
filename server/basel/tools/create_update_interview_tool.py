from typing import List, Optional
from uuid import UUID
from chromadb.api.models.Collection import logging
from llama_index.core.tools import FunctionTool
from pydantic import BaseModel, Field
from database.role import Role, RoleIdentifier
from database.user import User
from database.interview import Interview, InterviewType

logger = logging.getLogger(__name__)


class UpdateInterviewToolParams(BaseModel):
    interview_uuid: str = Field(
        description="The UUID of the interview of which to update. Can be fetched using the get_interviews tool if needed."
    )
    name: Optional[str] = Field(description="The given logical name of the interview.")
    description: Optional[str] = Field(description="The description of the interview.")
    interview_type: Optional[InterviewType] = Field(
        description="The type of interview."
    )
    tags: Optional[List[str]] = Field(description="Tags belonging to the interview.")
    position: Optional[str] = Field(
        description="The title of the position of which the interview is for."
    )
    status: Optional[bool] = Field(description="If the interview is active or not.")


async def update_interview(
    interview_uuid: str,
    user: User,
    role: Role,
    name: Optional[str] = None,
    description: Optional[str] = None,
    interview_type: Optional[InterviewType] = None,
    tags: Optional[List[str]] = None,
    position: Optional[str] = None,
    status: Optional[bool] = None,
):
    try:
        if role.identifier == RoleIdentifier.ADMIN:  # type:ignore
            interview = await Interview.find_one(Interview.uuid == UUID(interview_uuid))
        else:
            interview = await Interview.find_one(
                Interview.uuid == UUID(interview_uuid),
                Interview.created_by.id == user.id,  # type:ignore
            )

        if not interview:
            raise Exception("Interview not found.")

        interview.updated_by = user  # type:ignore

        if name:
            interview.name = name
        if description:
            interview.description = description
        if interview_type:
            interview.interview_type = interview_type
        if tags:
            interview.tags = tags
        if position:
            interview.position = position
        if status is not None:
            interview.status = status

        await interview.save()

        return interview

    except Exception as e:
        logger.error(e)
        return e


def create_update_interview_tool(current_user: User, role: Role):
    update_interview_tool = FunctionTool.from_defaults(
        name="update_interview_tool",
        description="Update an existing interview including name, organization name, description, interview type, tags, position and status.",
        async_fn=lambda interview_uuid, name, description, interview_type, tags, position, status: update_interview(
            interview_uuid=interview_uuid,
            user=current_user,
            role=role,
            name=name,
            description=description,
            interview_type=interview_type,
            tags=tags,
            position=position,
            status=status,
        ),
        fn_schema=UpdateInterviewToolParams,
    )
    return update_interview_tool
