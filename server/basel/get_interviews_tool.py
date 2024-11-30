import logging
from typing import List, Optional
from llama_index.core.bridge.pydantic import Field
from llama_index.core.tools.function_tool import FunctionTool
from classes.interview import Interview

from database.interview import InterviewModel
from database.user import UserModel

interview_model = InterviewModel("basel.db")
user_model = UserModel("basel.db")

logger = logging.getLogger(__name__)


def get_interviews(
    name_query: str = Field(
        description="""
        Search term that is used in the WHERE statement to find a specific interview by the name property.
        This term is automatically injected into a WILDCARD SQL Syntax, %term%, to improve search.
        """
    ),
    created_by_uuid: Optional[str] = Field(
        description="The uuid of the user who created the interview, useful to get interviews per user. Never provide ID or integer identifiers."
    ),
    limit: Optional[int] = Field(
        description="Limit the number of results returned. Default 10"
    ),
    offset: Optional[int] = Field(
        description="The number of results skipped for pagination. Default 0"
    ),
) -> List[Interview]:
    conn = interview_model._get_connection()
    cursor = conn.cursor()

    user = None
    if created_by_uuid:
        user = user_model.get_user_by_uuid(cursor, created_by_uuid)
        if not user:
            raise Exception("Can't find user.")

    interviews = interview_model.get_interviews(
        cursor,
        name=name_query,
        created_by=user.id if user else None,
        limit=limit,
        offset=offset,
    )

    conn.close()
    return interviews


def create_get_interviews_tool():
    get_interviews_tool = FunctionTool.from_defaults(
        fn=get_interviews,
        name="get_interiews_tool",
        description="""
        Fetch interview objects. Useful to get the name and description of interviews a user can take.
        """,
    )

    return get_interviews_tool
