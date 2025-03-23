import logging
from uuid import UUID
from functools import partial
from typing import List

from llama_index.core.bridge.pydantic import BaseModel, Field
from llama_index.core.tools.function_tool import FunctionTool
from llama_index.core.workflow import Context, HumanResponseEvent, InputRequiredEvent

from database.interview import Interview
from database.interview_question import InterviewQuestion
from database.user import User
from utils.validate import validate_uuid

logger = logging.getLogger(__name__)


class CreateInterviewQuestionsParams(BaseModel):
    interview_uuid: UUID = Field(
        description="The UUID of an interview to associate the question with."
    )
    questions: List[str] = Field(
        description="The questions associated with an interview that should be saved to the database"
    )


async def create_interview_questions(
    ctx: Context, current_user: User, interview_uuid: str, questions: List[str]
):
    try:
        pending_confirm = await ctx.get("pending_confirm_create_questions", False)
        logger.debug("CREATING QUESTIONS")

        is_valid_uuid = validate_uuid(interview_uuid)
        if not is_valid_uuid:
            raise Exception(
                "Invalid interview UUID. Ask the user to identify the target interview."
            )

        interview = await Interview.find_one(
            Interview.uuid == UUID(interview_uuid),
            Interview.created_by.id == current_user.id,  # type:ignore
        )
        if not interview:
            raise Exception(
                "Interview not found or user does not have permission to add questions to interivews they did not create."
            )

        if not pending_confirm:
            logger.debug("REQUESTING CONFIRM")
            await ctx.set("pending_confirm_create_questions", True)
            ctx.write_event_to_stream(
                InputRequiredEvent(
                    prefix=(
                        "Confirm the following questions should be added to the interview:\n"
                        + "".join(f"- {q}\n" for q in questions)
                        + "\nRespond with `yes` to add these questions to the interview."
                    )
                )
            )
        logger.debug("AWAITING CONFIRM")
        event = await ctx.wait_for_event(
            HumanResponseEvent,
        )
        await ctx.set("pending_confirm_create_questions", False)

        if event.response.lower() == "yes":
            logger.debug("CONFIRMED")
            interview_questions = [
                InterviewQuestion(
                    interview=interview,  # type:ignore
                    question=q,
                    created_by=current_user,  # type:ignore
                )
                for q in questions
            ]
            interview_question = await InterviewQuestion.insert_many(
                interview_questions
            )

            if not interview_question:
                raise Exception("Failed to create interview questions.")

            return "The questions has been saved to the database."
        else:
            logger.debug("REJECTED")
            return f"The user has provided additional input: {event.response}"

    except Exception as e:
        logger.error(e)
        raise e


def init_create_interview_questions_tool(current_user: User):
    create_interview_questions_tool = FunctionTool.from_defaults(
        async_fn=partial(create_interview_questions, current_user=current_user),
        name="create_interview_questions_tool",
        description="""
        Useful for adding a new question to interviews.
        """,
        fn_schema=CreateInterviewQuestionsParams,
    )
    return create_interview_questions_tool
