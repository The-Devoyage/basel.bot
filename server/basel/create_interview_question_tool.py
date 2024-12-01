import logging
from llama_index.core.bridge.pydantic import Field
from llama_index.core.tools.function_tool import FunctionTool

from database.interview_question import InterviewQuestionModel

interview_question_model = InterviewQuestionModel("basel.db")

logger = logging.getLogger(__name__)


def create_interview_question(
    current_user_id: int,
    interview_uuid: str = Field(
        description="The UUID of an interview to associate the question with."
    ),
    question: str = Field(description="The question associated with an interview."),
):
    conn = interview_question_model._get_connection()
    cursor = conn.cursor()
    interview_question_id = interview_question_model.create_interview_question(
        cursor, current_user_id, interview_uuid, question
    )
    conn.commit()
    if not interview_question_id:
        raise Exception("Failed to create interview question.")
    interview_question = interview_question_model.get_interview_question_by_id(
        cursor, interview_question_id
    )
    if not interview_question:
        raise Exception("Failed to find interview question")
    conn.close()
    return interview_question.to_public_dict()


def create_create_interview_question_tool(current_user_id: int):
    create_interview_question_tool = FunctionTool.from_defaults(
        fn=lambda interview_uuid, question: create_interview_question(
            current_user_id, interview_uuid, question
        ),
        name="create_interview_question_tool",
        description="Useful to create an associate a question to an intervview.",
    )
    return create_interview_question_tool
