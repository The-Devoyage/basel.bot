from chromadb.api.models.Collection import logging
from llama_index.core.tools.function_tool import FunctionTool
from llama_index.core.workflow import Context, HumanResponseEvent, InputRequiredEvent

logger = logging.getLogger(__name__)


async def pause_conduct_interview(ctx: Context):
    try:
        interview_in_progress = await ctx.get("interview_in_progress", False)
        if not interview_in_progress:
            return "Interview is not in progress."

        pending_pause_interview = await ctx.get("pending_pause_interview", False)
        if not pending_pause_interview:
            logger.debug("PENDING USER RESPONSE TO PAUSE INTERVIEW")
            await ctx.set("pending_pause_interview", True)
            ctx.write_event_to_stream(
                InputRequiredEvent(
                    prefix="I am detecting that you want to pause the interview. You can always come back later. Type `yes` to confirm that you'd like to stop the current interview."
                )
            )

        event = await ctx.wait_for_event(HumanResponseEvent)
        await ctx.set("pending_pause_interview", False)

        if event.response.lower() == "yes":
            logger.debug("PAUSING INTERVIEW")
            await ctx.set("interview_in_progress", False)
            await ctx.set("current_interview_uuid", None)
            return "The user has agreed to pause the interview."
        else:
            return f"Do not pause the interview. Keep the interview going. The user has responded: {event.response}"

    except Exception as e:
        logger.error(e)


def init_pause_conduct_interview_tool():
    pause_conduct_interview_tool = FunctionTool.from_defaults(
        name="pause_conduct_interview_tool",
        description="""
            Useful to transition out of an active interview that is not yet finished.
        """,
        async_fn=pause_conduct_interview,
    )
    return pause_conduct_interview_tool
