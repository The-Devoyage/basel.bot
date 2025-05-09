from typing import List, Optional
from uuid import UUID
from chromadb.api.models.Collection import logging
from llama_index.core.tools import FunctionTool
from pydantic import BaseModel, Field
from database.user import User
from database.interview import Interview, InterviewType

logger = logging.getLogger(__name__)


class UpdateInterviewToolParams(BaseModel):
    interview_uuid: str = Field(
        description="The UUID of the interview of which to update. Can be fetched using the get_interviews tool if needed."
    )
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
    description: Optional[str] = None,
    interview_type: Optional[InterviewType] = None,
    tags: Optional[List[str]] = None,
    position: Optional[str] = None,
    status: Optional[bool] = None,
):
    try:
        interview = await Interview.find_one(
            Interview.uuid == UUID(interview_uuid),
            Interview.created_by.id == user.id,  # type:ignore
        )

        if not interview:
            raise Exception("Interview not found.")

        interview.updated_by = user  # type:ignore

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


def create_update_interview_tool(current_user: User):
    update_interview_tool = FunctionTool.from_defaults(
        name="update_interview_tool",
        description="""
        Update an existing interview including the following fields:
        - description: A short summary about the interview.
        - interview type: If the interview is a general or application rated.
        - tags: Key words to organize interviews.
        - position: The name of the position the interview is for.
        - status: If the interview is enabled or disabled.
        """,
        async_fn=lambda interview_uuid, description, interview_type, tags, position, status: update_interview(
            interview_uuid=interview_uuid,
            user=current_user,
            description=description,
            interview_type=interview_type,
            tags=tags,
            position=position,
            status=status,
        ),
        fn_schema=UpdateInterviewToolParams,
    )
    return update_interview_tool
