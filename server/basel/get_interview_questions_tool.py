import logging
from llama_index.core.bridge.pydantic import Field
from llama_index.core.tools.function_tool import FunctionTool

from database.interview_question import InterviewQuestionModel

interview_question_model = InterviewQuestionModel("basel.db")

logger = logging.getLogger(__name__)


def get_interview_questions(
    interview_uuid: str = Field(
        description="The UUID of the interview to get questions for."
    ),
):
    conn = interview_question_model._get_connection()
    cursor = conn.cursor()
    interview_questions = interview_question_model.get_interview_questions(
        cursor, interview_uuid=interview_uuid
    )
    conn.close()
    return interview_questions


def create_get_interview_questions_tool():
    get_interview_questions_tool = FunctionTool.from_defaults(
        fn=get_interview_questions,
        name="get_interview_questions_tool",
        description="Useful to get questions associated with an interview.",
    )
    return get_interview_questions_tool
