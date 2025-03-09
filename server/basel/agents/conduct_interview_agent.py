from llama_index.core.agent.workflow import FunctionAgent
from basel.tools.ask_interview_question_tool import create_ask_interview_question_tool
from basel.tools.create_get_interview_question_response_tool import (
    create_get_interview_question_responses_tool,
)
from basel.tools.create_upsert_interview_question_response_tool import (
    create_upsert_interview_question_response_tool,
)
from basel.tools.get_interview_questions_tool import create_get_interview_questions_tool
from basel.tools.get_interviews_tool import create_get_interviews_tool

from database.user import User


def init_conduct_interview_agent(current_user: User):
    tools = []

    get_interview_questions_tool = create_get_interview_questions_tool()
    tools.append(get_interview_questions_tool)

    get_interviews_tool = create_get_interviews_tool()
    tools.append(get_interviews_tool)

    if current_user:
        # Get Interview Question Responses
        get_interview_question_responses_tool = (
            create_get_interview_question_responses_tool(current_user)
        )
        tools.append(get_interview_question_responses_tool)

        # Upsert interview question response
        upsert_interview_question_response_tool = (
            create_upsert_interview_question_response_tool(current_user)
        )
        tools.append(upsert_interview_question_response_tool)

        # Ask interview question tool
        # ask_interview_question_tool = create_ask_interview_question_tool(current_user)
        # tools.append(ask_interview_question_tool)

    conduct_interview_agent = FunctionAgent(
        name="conduct_interview_agent",
        description="Useful for conducting an interviews and saving user responses.",
        system_prompt="""
            You are the conduct_interview_agent that can ask interview questions to the candidate and collect/save their responses.
            Pick up where the user left off with the interview and ask the user all of the questions. Hand off to the submit_interview_agent
            when the user is done.
        """,
        tools=tools,
        can_handoff_to=["submit_interview_agent"],
    )
    return conduct_interview_agent
