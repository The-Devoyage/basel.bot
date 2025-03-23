from datetime import datetime
from functools import partial
from uuid import UUID
from llama_index.core.bridge.pydantic import BaseModel, Field
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai.utils import logging
from database.interview_transcript import InterviewTranscript
from database.message import SenderIdentifer
from database.user import User
from llama_index.core.workflow import Context

logger = logging.getLogger(__name__)


class InterviewTranscriptSort(BaseModel):
    transcript: str
    sender: SenderIdentifer
    created_at: datetime


class GetInterviewTranscriptParams(BaseModel):
    interview_uuid: UUID = Field(
        description="The UUID of the interview with associated transcripts."
    )


async def get_interview_transcript(
    ctx: Context, chatting_with: User, interview_uuid: str
):
    try:
        interview_assessment = await ctx.get("interview_assessment", None)

        logger.debug(f"DEFAULT ASSESSMENT: {interview_assessment}")

        query = InterviewTranscript.find(
            InterviewTranscript.user.id == chatting_with.id,  # type:ignore
            InterviewTranscript.interview.uuid  # type:ignore
            == UUID(interview_uuid),
            fetch_links=True,
        )

        if interview_assessment:
            query.find(
                InterviewTranscript.interview.id  # type:ignore
                == interview_assessment.interview.id,
                fetch_links=True,
            )

        interview_transcript = await query.project(InterviewTranscriptSort).to_list()

        return interview_transcript
    except Exception as e:
        logger.error(e)
        raise Exception("Failed to fetch interview transcript.")


def init_get_interview_transcript_tool(chatting_with: User):
    get_interview_transcript_tool = FunctionTool.from_defaults(
        name="get_interview_transcript_tool",
        description="Useful to fetch the transcript of an interview.",
        async_fn=partial(get_interview_transcript, chatting_with=chatting_with),
        fn_schema=GetInterviewTranscriptParams,
    )
    return get_interview_transcript_tool
