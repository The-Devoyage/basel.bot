from datetime import datetime
from functools import partial
from uuid import UUID
from llama_index.agent.openai.openai_assistant_agent import json
from llama_index.core.tools import FunctionTool
from pydantic import BaseModel, Field
import logging
from classes.socket_message import MessageType, SocketMessage
from database.interview_question import InterviewQuestion
from database.interview_question_response import InterviewQuestionResponse
from database.message import SenderIdentifer
from database.user import User
from llama_index.core.workflow import Context, HumanResponseEvent, InputRequiredEvent
from utils.brokers import ws_broker

logger = logging.getLogger(__name__)


class AskInterviewQuestionParams(BaseModel):
    interview_question_uuid: str = Field(
        description="The UUID of the interview question to ask the user."
    )


async def ask_interview_question(
    ctx: Context, user: User, interview_question_uuid: str
):
    try:
        logger.debug("ASKING QUESTION")
        question_asked = await ctx.get("question_asked", False)
        if not question_asked:
            interview_question = await InterviewQuestion.find_one(
                InterviewQuestion.uuid == UUID(interview_question_uuid)
            )

            if not interview_question:
                raise Exception("Failed to find interview question.")

            response = await InterviewQuestionResponse.find_one(
                InterviewQuestionResponse.interview_question.id  # type:ignore
                == interview_question.id,
                InterviewQuestionResponse.user.id  # type:ignore
                == user.id,
                fetch_links=True,
            )

            card = json.dumps(
                {
                    "header": "Question",
                    "response": response.response if response else None,
                    "interview_question": await interview_question.to_public_dict(),
                },
                default=str,
            )

            response = SocketMessage(
                text=card,
                message_type=MessageType.CARD,
                timestamp=datetime.now(),
                sender=SenderIdentifer.BOT,
                buttons=None,
            )

            # if user.uuid not in ui_events:
            # ui_events[user.uuid] = []

            # Append the new question event to the list
            # ui_events[user.uuid].append(response.model_dump_json())
            await ws_broker[user.uuid].send_text(response.model_dump_json())
            # await websocket.send_text(response.model_dump_json())

            logger.debug("WAITING FOR QUESTION RESPONSE")
            await ctx.set("question_asked", True)
            ctx.write_event_to_stream(
                InputRequiredEvent(
                    prefix="After you answer, let me know and I'll ask the next question.",
                )
            )

        response = await ctx.wait_for_event(HumanResponseEvent)

        logger.debug("NEXT QUESTION")

        return "The user has been asked the question. Ask the next question using the ask_interview_question_tool."

    except Exception as e:
        logger.error(e)
        return f"Something went wrong when asking the question. Bail on the interview: {str(e)}"


def create_ask_interview_question_tool(user: User):
    ask_interview_question_tool = FunctionTool.from_defaults(
        name="ask_interview_question_tool",
        description="""
        Use this tool in order to ask questions when a user requests to take an interview. Providing the question UUID to this tool
        will trigger a UI event that allows the user to submit a response to the question.
        """,
        async_fn=partial(ask_interview_question, user=user),
        fn_schema=AskInterviewQuestionParams,
    )

    return ask_interview_question_tool
