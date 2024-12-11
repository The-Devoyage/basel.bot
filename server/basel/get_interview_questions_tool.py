import logging
from llama_index.core.bridge.pydantic import Field
from llama_index.core.tools.function_tool import FunctionTool
from database.interview import Interview

from database.interview_question import InterviewQuestion

logger = logging.getLogger(__name__)


async def get_interview_questions(
    interview_uuid: str = Field(
        description="The UUID of the interview to get questions for."
    ),
):
    interview_questions = await InterviewQuestion.find(
        InterviewQuestion.interview.uuid == interview_uuid  # type:ignore
    ).to_list()
    return interview_questions


def create_get_interview_questions_tool():
    get_interview_questions_tool = FunctionTool.from_defaults(
        fn=get_interview_questions,
        name="get_interview_questions_tool",
        description="Useful to get questions associated with an interview.",
    )
    return get_interview_questions_tool
