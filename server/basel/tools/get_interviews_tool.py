from typing import List, Optional
from llama_index.core.bridge.pydantic import Field
from llama_index.core.tools.function_tool import FunctionTool
from llama_index.llms.openai.utils import BaseModel

from database.interview import Interview


class GetInterviewsParams(BaseModel):
    search_term: Optional[str] = Field(
        default=None,
        description="""
        Search term that is used in the query statement to find a specific interview by the name property.
        This term is automatically injected into a REGEX syntax for you.
        """,
    )
    limit: Optional[int] = Field(
        default=10, description="Limit the number of results returned. Default 10"
    )
    offset: Optional[int] = Field(
        default=0, description="The number of results skipped for pagination. Default 0"
    )


async def get_interviews(search_term=None, limit=10, offset=0):
    interviews = Interview.find().limit(limit).skip(offset)

    if search_term:
        interviews.find({"name": {"$regex": search_term, "$options": "i"}})

    interviews = await interviews.to_list()

    interviews = [await interview.to_public_dict() for interview in interviews]

    return interviews


def create_get_interviews_tool():
    get_interviews_tool = FunctionTool.from_defaults(
        async_fn=get_interviews,
        name="get_interiews_tool",
        description="""
        Fetch interview objects. Useful to get the name and description of interviews a user can take.
        """,
        fn_schema=GetInterviewsParams,
    )

    return get_interviews_tool
