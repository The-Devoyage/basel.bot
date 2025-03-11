from chromadb.api.models.Collection import logging
from llama_index.core.tools import FunctionTool
from llama_index.core.workflow import Context, HumanResponseEvent, InputRequiredEvent

logger = logging.getLogger(__name__)


async def start_conduct_interview(ctx: Context):
    try:
        interview_in_progress = await ctx.get("interview_in_progress", False)
        if interview_in_progress:
            return "Interview is already in progress. Proceed to ask questions using the `ask_interview_question_tool`"

        pending_start_interview = await ctx.get("pending_start_interview", False)
        if not pending_start_interview:
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
            return "The user has agreed to start the interview. Proceed to ask them questions using the `ask_interview_questions_tool`."
        else:
            return (
                f"Do not start the interview. The user has responded: {event.response}"
            )

    except Exception as e:
        logger.error(e)


def init_start_conduct_interview_tool():
    start_conduct_interview_tool = FunctionTool.from_defaults(
        name="start_conduct_interview_tool",
        async_fn=start_conduct_interview,
        description="""
            Use this tool to confirm that the user is ready to begin the interview.
        """,
    )
    return start_conduct_interview_tool
