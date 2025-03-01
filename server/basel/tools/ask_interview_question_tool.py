from datetime import datetime
from uuid import UUID
from fastapi import WebSocket
from llama_index.agent.openai.openai_assistant_agent import json
from llama_index.core.tools import FunctionTool
from pydantic import BaseModel, Field
import logging
from classes.socket_message import MessageType, SocketMessage

from database.interview_question import InterviewQuestion
from database.interview_question_response import InterviewQuestionResponse
from database.message import SenderIdentifer
from database.user import User

logger = logging.getLogger(__name__)


class AskInterviewQuestionParams(BaseModel):
    interview_question_uuid: str = Field(
        description="The UUID of the interview question to ask the user."
    )


async def ask_interview_question(
    websocket: WebSocket, user: User, interview_question_uuid
):
    try:
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

        await websocket.send_text(response.model_dump_json())

        return "The user has been asked the question."

    except Exception as e:
        logger.error(e)
        return f"Something went wrong when asking the question: {str(e)}"


def create_ask_interview_question_tool(websocket: WebSocket, user: User):
    ask_interview_question_tool = FunctionTool.from_defaults(
        name="ask_interview_question_tool",
        description="""
        Use this tool in order to ask questions when a user requests to take an interview. Providing the question UUID to this tool
        will trigger a UI event that allows the user to submit a response to the question.
        """,
        async_fn=lambda interview_question_uuid: ask_interview_question(
            websocket=websocket,
            interview_question_uuid=interview_question_uuid,
            user=user,
        ),
        fn_schema=AskInterviewQuestionParams,
    )

    return ask_interview_question_tool
