from uuid import UUID
from chromadb.api.models.Collection import logging
from llama_index.core.bridge.pydantic import BaseModel, Field
from llama_index.core.tools.function_tool import FunctionTool
from database.interview_question_response import InterviewQuestionResponse

from database.user import User

logger = logging.getLogger(__name__)


class GetInterviewQuestionResponsesParams(BaseModel):
    interview_uuid: str = Field(
        description="The UUID of the interview the interview that the questions belong to."
    )


async def get_interview_question_responses(user: User, interview_uuid: str):
    interview_question_responses = await InterviewQuestionResponse.find(
        InterviewQuestionResponse.interview_question.interview.uuid  # type:ignore
        == UUID(interview_uuid),
        InterviewQuestionResponse.user.id == user.id,  # type:ignore
        fetch_links=True,
    ).to_list()

    return [
        await response.to_public_dict() for response in interview_question_responses
    ]


def create_get_interview_question_responses_tool(user: User):
    get_interview_question_response_tool = FunctionTool.from_defaults(
        async_fn=lambda interview_uuid: get_interview_question_responses(
            user,
            interview_uuid,
        ),
        name="get_interview_question_responses_tool",
        description="""
        Useful to get interview question responses by interview for a specific user.
        """,
        fn_schema=GetInterviewQuestionResponsesParams,
    )

    return get_interview_question_response_tool
