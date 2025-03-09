from typing import Optional
from llama_index.core.agent.workflow import FunctionAgent
from basel.tools.create_get_interview_question_response_tool import (
    create_get_interview_question_responses_tool,
)

from basel.tools.get_interview_questions_tool import create_get_interview_questions_tool
from basel.tools.get_interviews_tool import create_get_interviews_tool
from database.user import User


def init_interview_retriever_agent(chatting_with: Optional[User]):
    tools = []

    get_interview_questions_tool = create_get_interview_questions_tool()
    tools.append(get_interview_questions_tool)

    get_interviews_tool = create_get_interviews_tool()
    tools.append(get_interviews_tool)

    if chatting_with:
        get_interview_question_responses_tool = (
            create_get_interview_question_responses_tool(chatting_with)
        )
        tools.append(get_interview_question_responses_tool)

    agent = FunctionAgent(
        name="interview_retriever_agent",
        description="Useful to lookup interviews.",
        system_prompt="""
            - You are the Interview Retriever Agent that can query the database for interviews and/or the questions belonging to an interview.
            - Use the `get_interview_tool` to get high level details about the interview such as the name, description, and status.
            - Use  the `get_interview_questions_tool` to get the questions associated with an interview.
            - Use the `get_interview_question_responses_tool` to get the responses or answers that the candidate has provided for each question.
        """,
        tools=tools,
    )

    return agent
