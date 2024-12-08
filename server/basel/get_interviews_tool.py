import logging
from typing import List, Optional
from llama_index.core.bridge.pydantic import Field
from llama_index.core.tools.function_tool import FunctionTool

from database.interview import Interview
from database.user import User

logger = logging.getLogger(__name__)


async def get_interviews(
    name_query: str = Field(
        description="""
        Search term that is used in the WHERE statement to find a specific interview by the name property.
        This term is automatically injected into a WILDCARD SQL Syntax, %term%, to improve search.
        """
    ),
    limit: Optional[int] = Field(
        description="Limit the number of results returned. Default 10"
    ),
    offset: Optional[int] = Field(
        description="The number of results skipped for pagination. Default 0"
    ),
) -> List[Interview]:
    interviews = (
        await Interview.find(name=name_query).limit(limit).skip(offset).to_list()
    )

    return interviews


def create_get_interviews_tool():
    get_interviews_tool = FunctionTool.from_defaults(
        async_fn=get_interviews,
        name="get_interiews_tool",
        description="""
        Fetch interview objects. Useful to get the name and description of interviews a user can take.
        """,
    )

    return get_interviews_tool
