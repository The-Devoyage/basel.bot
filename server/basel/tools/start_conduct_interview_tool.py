from datetime import datetime
from functools import partial
from uuid import UUID
from chromadb.api.models.Collection import logging
from llama_index.core.tools import FunctionTool
from llama_index.core.workflow import Context, HumanResponseEvent, InputRequiredEvent
from pydantic import BaseModel, Field

from database.interview import Interview
from database.interview_transcript import InterviewTranscript
from database.message import SenderIdentifer
from database.user import User

logger = logging.getLogger(__name__)


class StartConductInterviewParams(BaseModel):
    interview_uuid: UUID = Field(
        description="The UUID of the interview the user wants to take."
    )


class InterviewTranscriptShort(BaseModel):
    sender: SenderIdentifer
    transcript: str
    created_at: datetime


async def start_conduct_interview(
    ctx: Context, interview_uuid: str, current_user: User
):
    try:
        interview_in_progress = await ctx.get("interview_in_progress", False)
        if interview_in_progress:
            return "Interview is already in progress. Proceed to ask questions using the `ask_interview_question_tool`"

        # Check if interview exists
        interview = await Interview.find_one(Interview.uuid == UUID(interview_uuid))
        if not interview:
            return "Interview could not be found. Please try again."

        pending_start_interview = await ctx.get("pending_start_interview", False)
        if not pending_start_interview:
            await ctx.set("current_interview_uuid", interview.uuid)
            logger.debug("PENDING USER RESPONSE TO START INTERVIEW")
            await ctx.set("pending_start_interview", True)
            ctx.write_event_to_stream(
                InputRequiredEvent(
                    prefix="I am detecting that you want to start the interview. You can always pause while in progress. Type `yes` to confirm that you'd like to start the interview."
                )
            )

        event = await ctx.wait_for_event(HumanResponseEvent)
        await ctx.set("pending_start_interview", False)

        if event.response.lower() == "yes":
            logger.debug("STARTING INTERVIEW")
            await ctx.set("interview_in_progress", True)

            interview_transcripts = (
                await InterviewTranscript.find(
                    InterviewTranscript.interview.id == interview.id,  # type:ignore
                    InterviewTranscript.user.id == current_user.id,  # type:ignore
                )
                .project(InterviewTranscriptShort)
                .to_list()
            )

            return f"""
                The user has agreed to start the interview. 
                Proceed to ask them questions using the `ask_interview_questions_tool`.

                Current Transcript: {interview_transcripts}
            """
        else:
            return (
                f"Do not start the interview. The user has responded: {event.response}"
            )

    except Exception as e:
        logger.error(e)


def init_start_conduct_interview_tool(current_user: User):
    start_conduct_interview_tool = FunctionTool.from_defaults(
        name="start_conduct_interview_tool",
        async_fn=partial(start_conduct_interview, current_user=current_user),
        description="""
            Use this tool to confirm that the user is ready to begin the interview.
        """,
        fn_schema=StartConductInterviewParams,
    )
    return start_conduct_interview_tool
