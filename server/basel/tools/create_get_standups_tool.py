import logging
from typing import Optional
from beanie import SortDirection
from llama_index.core.bridge.pydantic import BaseModel, Field
from llama_index.core.tools.function_tool import FunctionTool
from database.user import User
from database.standup import Standup

logger = logging.getLogger(__name__)


class GetStandupsParams(BaseModel):
    limit: Optional[int] = Field(
        description="How many to limit for pagination. Default 10"
    )
    offset: Optional[int] = Field(
        description="How many to skip for pagination. Default 0"
    )


async def get_standups(user: User, offset, limit):
    logger.debug(f"USER: {user}")
    try:
        standups = (
            await Standup.find(
                Standup.user.id == user.id, fetch_links=True  # type:ignore
            )
            .limit(limit)
            .skip(offset)
            .sort([(Standup.created_at, SortDirection.DESCENDING)])  # type:ignore
            .to_list()
        )

        logger.debug(f"STANDUPS: {standups}")
        return [await standup.to_public_dict() for standup in standups]

    except Exception as e:
        logger.error(e)
        return "Something went wrong when getting standups."


def create_get_standups_tool(user: User):
    get_standups_tool = FunctionTool.from_defaults(
        async_fn=lambda limit, offset: get_standups(user, offset, limit),
        name="get_standups_tool",
        description="Useful to get standups previously logged by the current user.",
        fn_schema=GetStandupsParams,
    )
    return get_standups_tool
