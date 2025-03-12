from functools import partial
from llama_index.core.tools import FunctionTool
from pydantic import BaseModel, Field
import logging
from database.interview import Interview
from database.message import SenderIdentifer
from database.user import User
from database.interview_transcript import InterviewTranscript
from llama_index.core.workflow import Context, HumanResponseEvent, InputRequiredEvent

logger = logging.getLogger(__name__)


class AskInterviewQuestionParams(BaseModel):
    question_prompt: str = Field(
        description="The prompt, containing the interview question, to send the user."
    )


async def ask_interview_question(ctx: Context, user: User, question_prompt: str):
    try:
        logger.debug("ASKING QUESTION")
        interview_in_progress = await ctx.get("interview_in_progress", False)

        if not interview_in_progress:
            return "Before asking questions, confirm with the user that they want to start the interview using the `start_conduct_interview_tool`."

        current_interview_uuid = await ctx.get("current_interview_uuid", None)
        if not current_interview_uuid:
            return "Current interview not selected. Please start the interview over to select an interview."
        interview = await Interview.find_one(Interview.uuid == current_interview_uuid)
        logger.debug(f"CURRENT INTERVIEW UUID: {current_interview_uuid}")
        if not interview:
            return "Interview was not found by the currently selected interview."

        pending_question_response = await ctx.get("pending_question_response", False)
        await ctx.set("interview_in_progress", True)
        logger.debug(f"QUESTION ASKED: {pending_question_response}")
        if not pending_question_response:
            await InterviewTranscript(
                user=user,  # type:ignore
                interview=interview,  # type:ignore
                transcript=f"Bot: {question_prompt}",
                created_by=user,  # type:ignore
                sender=SenderIdentifer.BOT,
            ).create()

            logger.debug("WAITING FOR QUESTION RESPONSE")
            logger.debug(f"NEW INTERVIEW QUESTION: {question_prompt}")
            await ctx.set("pending_question_response", True)
            ctx.write_event_to_stream(
                InputRequiredEvent(
                    prefix=question_prompt,
                )
            )

        event = await ctx.wait_for_event(HumanResponseEvent)
        await ctx.set("pending_question_response", False)

        if event.response:
            await InterviewTranscript(
                user=user,  # type:ignore
                interview=interview,  # type:ignore
                transcript=event.response,
                created_by=user,  # type:ignore
                sender=SenderIdentifer.USER,
            ).create()

            logger.debug("NEXT QUESTION")
            return f"""
                The user responded: {event.response}

                Continue the interview by using the ask_interview_question_tool.
            """
        else:
            raise Exception("Failed to collect response")

    except Exception as e:
        logger.debug(f"ERROR: {e}")
        raise Exception(f"Something went wrong when asking the question.: {str(e)}")


def init_ask_interview_question_tool(user: User):
    ask_interview_question_tool = FunctionTool.from_defaults(
        name="ask_interview_question_tool",
        description="""
            Use this tool in order to ask questions to a user requests during an interview. Responses are automatically saved.
            You may rephrase quesions, including contextual details.

            Example:
            question_prompt: "It's great to hear you are into xyz. Do you find xyz to be beneficial to abc?"
        """,
        async_fn=partial(ask_interview_question, user=user),
        fn_schema=AskInterviewQuestionParams,
    )

    return ask_interview_question_tool
