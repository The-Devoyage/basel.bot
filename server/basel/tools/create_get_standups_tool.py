from dateutil import parser
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
    start_date: Optional[str] = Field(
        description="Search for interviews created on or after this date."
    )
    end_date: Optional[str] = Field(
        description="Search for interviews created before or equivelant to this date.",
    )


async def get_standups(
    user: User,
    offset=0,
    limit=10,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
):
    try:
        logger.debug(f"DATES: {start_date} {end_date}")
        query = Standup.find(
            Standup.user.id == user.id, fetch_links=True  # type:ignore
        )

        if start_date:
            fstart = parser.parse(start_date)
            query.find(Standup.created_at >= fstart)
        if end_date:
            fend = parser.parse(end_date)
            query.find(Standup.created_at <= fend)

        standups = await (
            query.limit(limit)
            .skip(offset)
            .sort([(Standup.created_at, SortDirection.DESCENDING)])  # type:ignore
            .to_list()
        )

        return [await standup.to_public_dict() for standup in standups]

    except Exception as e:
        logger.error(e)
        return "Something went wrong when getting standups."


def create_get_standups_tool(user: User):
    get_standups_tool = FunctionTool.from_defaults(
        async_fn=lambda limit, offset, start_date, end_date: get_standups(
            user=user,
            offset=offset,
            limit=limit,
            start_date=start_date,
            end_date=end_date,
        ),
        name="get_standups_tool",
        description="Useful to get standups previously logged by the current user.",
        fn_schema=GetStandupsParams,
    )
    return get_standups_tool
