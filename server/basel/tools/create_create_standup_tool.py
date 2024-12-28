from typing import Optional
from chromadb.api.models.Collection import logging
from llama_index.core.tools import FunctionTool
from pydantic import BaseModel

from database.standup import Standup
from database.user import User

logger = logging.getLogger(__name__)


class CreateStandupParams(BaseModel):
    yesterday: Optional[str]
    today: Optional[str]
    blockers: Optional[str]


async def create_standup(yesterday, today, blockers, user):
    try:
        standup = await Standup(
            yesterday=yesterday,
            today=today,
            blockers=blockers,
            user=user,
            created_by=user,
        ).create()

        return standup.to_public_dict()
    except Exception as e:
        logger.error(e)
        return "Failed to create standup."


def create_create_standup_tool(user: User):
    create_standup_tool = FunctionTool.from_defaults(
        async_fn=lambda yesterday, today, blockers: create_standup(
            yesterday, today, blockers, user
        ),
        name="create_standup_tool",
        description="Useful to assist a user log a standup which is encouraged for them to do at least once a day (weekdays).",
        fn_schema=CreateStandupParams,
    )
    return create_standup_tool
