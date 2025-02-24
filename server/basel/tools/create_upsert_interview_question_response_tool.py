from uuid import UUID
from beanie.operators import Set
from llama_index.core.bridge.pydantic import BaseModel, Field
from llama_index.core.tools.function_tool import FunctionTool
from database.interview_assessment import InterviewAssessment
from database.interview_question import InterviewQuestion
from database.interview_question_response import InterviewQuestionResponse
import logging
from database.user import User

logger = logging.getLogger(__name__)


class UpsertInterviewQuestionResponseParams(BaseModel):
    interview_question_uuid: str = Field(
        description="""
            - The UUID of the interview_question being answered. 
            - Use the `get_interview_questions` tool to get the uuid, if needed. 
            - Do not submit integers.
            - If you don't have the UUID, simply instuct the user to start over from the interviews screen.
        """
    )
    response: str = Field(
        description="""
            The response the user provides, in their own words and language. This should not be altered or summerized
        """
    )


async def upsert_interview_question_response(
    user: User, interview_question_uuid: str, response: str
):
    try:
        interview_question = await InterviewQuestion.find_one(
            InterviewQuestion.uuid == UUID(interview_question_uuid), fetch_links=True
        )

        if not interview_question:
            raise Exception("Interview question not found.")

        interview_assessment = await InterviewAssessment.find_one(
            InterviewAssessment.interview.id  # type:ignore
            == interview_question.interview.id,  # type:ignore
            InterviewAssessment.user.id == user.id,  # type:ignore
        )

        if interview_assessment:
            raise Exception(
                "User has completed and sumbitted this entire interview and no further questions can not be updated/submitted at this time."
            )

        updated = await InterviewQuestionResponse.find_one(
            InterviewQuestionResponse.user.id == user.id,  # type:ignore
            InterviewQuestionResponse.interview_question.id  # type:ignore
            == interview_question.id,
        ).upsert(
            Set({"response": response}),
            on_insert=InterviewQuestionResponse(
                user=user,  # type:ignore
                interview_question=interview_question,  # type:ignore
                created_by=user,  # type:ignore
                response=response,
            ),
        )

        # Handle Errors
        if not updated:
            raise Exception("Failed to upsert interview question response.")

        interview_question_response = await InterviewQuestionResponse.find_one(
            InterviewQuestionResponse.user.id == user.id,  # type:ignore
            InterviewQuestionResponse.interview_question.id  # type:ignore
            == interview_question.id,
        )

        if not interview_question_response:
            raise Exception("Failed to find interview question response.")

        return await interview_question_response.to_public_dict()
    except Exception as e:
        logger.error(e)
        return "Failed to create or update response. Error: " + str(e)


def create_upsert_interview_question_response_tool(user: User):
    upsert_interview_question_response_tool = FunctionTool.from_defaults(
        async_fn=lambda response, interview_question_uuid: upsert_interview_question_response(
            user=user,
            interview_question_uuid=interview_question_uuid,
            response=response,
        ),
        name="upsert_interview_question_response_tool",
        description="""
            - Useful for saving user responses to interview questions.
            - Do not alter the user input - save the exact response from the user.
            """,
        fn_schema=UpsertInterviewQuestionResponseParams,
    )

    return upsert_interview_question_response_tool
