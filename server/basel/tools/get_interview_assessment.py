from functools import partial
from uuid import UUID
from llama_index.core.bridge.pydantic import BaseModel, Field
from llama_index.core.tools import FunctionTool
from database.interview_assessment import InterviewAssessment
from database.user import User
import logging

logger = logging.getLogger(__name__)


class GetInterviewAssessmentParams(BaseModel):
    interview_uuid: UUID = Field(
        description="The UUID of the interview of the associated assessment."
    )


async def get_interview_assessment(chatting_with: User, interview_uuid: str):
    try:
        interview_assessment = await InterviewAssessment.find_one(
            InterviewAssessment.interview.uuid == UUID(interview_uuid),  # type:ignore
            InterviewAssessment.user.id == chatting_with.id,  # type:ignore
            fetch_links=True,
        )
        return interview_assessment
    except Exception as e:
        logger.error(e)
        raise Exception("Failed to fetch interview assessment.")


def init_get_interview_assessment_tool(chatting_with: User):
    get_interview_assessment_tool = FunctionTool.from_defaults(
        name="get_interview_assessment_tool",
        description="""
            Get the final assessment of an interview for the candidate.
            Includes Ratings:
            - overall
            - content_relevance 
            - communication_skills
            - confidence_delivery
            - structure_organization
            - adaptability_critical_thinking
            - technical_industry_knowledge
        """,
        async_fn=partial(get_interview_assessment, chatting_with=chatting_with),
        fn_schema=GetInterviewAssessmentParams,
    )

    return get_interview_assessment_tool
