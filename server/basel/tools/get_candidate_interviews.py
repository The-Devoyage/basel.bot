from functools import partial
from uuid import UUID
from llama_index.core.bridge.pydantic import BaseModel, Field
from beanie.operators import In
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai.utils import logging
from llama_index.core.workflow import Context

from database.interview import Interview, get_pipeline
from database.user import User

logger = logging.getLogger(__name__)


class InterviewShortView(BaseModel):
    uuid: UUID
    position: str


class GetCandidateInterviewsParams(BaseModel):
    limit: int = Field(
        default=10,
        description="Pagination limit control for the number of items per page.",
    )
    skip: int = Field(
        default=0, description="Pagionation control for the offset of interviews."
    )


async def get_candidate_interviews(
    ctx: Context,
    chatting_with: User,
    limit: int = 10,
    skip: int = 0,
):
    try:
        query = Interview.find()

        interview_assessment = await ctx.get("interview_assessment", None)
        shareable_link = await ctx.get("shareable_link", None)

        if interview_assessment:
            query.find(Interview.id == interview_assessment.interview.id)

        if shareable_link:
            query.find(
                In(
                    Interview.id,
                    [interview.id for interview in shareable_link.interviews],
                )
            )

        if not interview_assessment and not shareable_link:
            pipeline = get_pipeline(
                user_id=chatting_with.id if chatting_with else None,
                taken_by_me=True,
                shareable_link_id=None,
            )
            query.aggregate(pipeline)

        interviews = (
            await query.project(InterviewShortView).limit(limit).skip(skip).to_list()
        )
        return interviews
    except Exception as e:
        logger.error(e)
        raise e


def init_get_candidate_interviews_tool(chatting_with: User):
    get_candidate_interviews_tool = FunctionTool.from_defaults(
        name="get_candidate_interviews_tool",
        description="""
            Useful to fetch interviews that the candidate has taken.
        """,
        async_fn=partial(get_candidate_interviews, chatting_with=chatting_with),
        fn_schema=GetCandidateInterviewsParams,
    )
    return get_candidate_interviews_tool
