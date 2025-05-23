from uuid import UUID
from llama_index.core.bridge.pydantic import Field
from llama_index.core.tools.function_tool import FunctionTool
from llama_index.llms.openai.utils import BaseModel

from database.interview_question import InterviewQuestion


class GetInterviewQuestionsParams(BaseModel):
    interview_uuid: str = Field(
        description="The UUID of the interview to get questions for. Get the UUID using the get_interval_tool if needed."
    )


class InterviewQuestionShortView(BaseModel):
    uuid: UUID
    question: str


async def get_interview_questions(interview_uuid):
    interview_questions = (
        await InterviewQuestion.find(
            InterviewQuestion.interview.uuid == UUID(interview_uuid),  # type:ignore
            # InterviewQuestion.status == True,
            fetch_links=True,
        )
        .project(InterviewQuestionShortView)
        .to_list()
    )
    return interview_questions


def create_get_interview_questions_tool():
    get_interview_questions_tool = FunctionTool.from_defaults(
        async_fn=get_interview_questions,
        fn_schema=GetInterviewQuestionsParams,
        name="get_interview_questions_tool",
        description="Useful to get questions associated with an interview.",
    )
    return get_interview_questions_tool
