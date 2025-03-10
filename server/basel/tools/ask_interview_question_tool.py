from functools import partial
from llama_index.core.tools import FunctionTool
from pydantic import BaseModel, Field
import logging
from database.user import User
from llama_index.core.workflow import Context, HumanResponseEvent, InputRequiredEvent

logger = logging.getLogger(__name__)


class AskInterviewQuestionParams(BaseModel):
    question_prompt: str = Field(
        description="The prompt, containing the interview question, to send the user."
    )


async def ask_interview_question(ctx: Context, user: User, question_prompt: str):
    try:
        logger.debug("ASKING QUESTION")
        question_asked = await ctx.get("question_asked", False)
        logger.debug(f"QUESTION ASKED: {question_asked}")
        if not question_asked:
            logger.debug("WAITING FOR QUESTION RESPONSE")
            logger.debug(f"NEW INTERVIEW QUESTION: {question_prompt}")
            await ctx.set("question_asked", True)
            ctx.write_event_to_stream(
                InputRequiredEvent(
                    prefix=question_prompt,
                )
            )

        event = await ctx.wait_for_event(HumanResponseEvent)
        await ctx.set("question_asked", False)

        if event.response:
            logger.debug("NEXT QUESTION")
            return f"The user responded: {event.response}"
        else:
            raise Exception("Failed to collect response")

    except Exception as e:
        logger.error(e)
        raise Exception(f"Something went wrong when asking the question.: {str(e)}")


def create_ask_interview_question_tool(user: User):
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
