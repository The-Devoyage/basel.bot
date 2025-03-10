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

    # Ask interview question tool
    ask_interview_question_tool = create_ask_interview_question_tool(current_user)
    tools.append(ask_interview_question_tool)

    conduct_interview_agent = FunctionAgent(
        name="conduct_interview_agent",
        description="Useful for conducting an interviews and saving user responses.",
        system_prompt="""
            You are the conduct_interview_agent that asks interview questions to the user.  
            - Use the `get_interview_questions_tool` to get the pre-determined questions to ask.
            - Use the `ask_interview_question_tool` to ask the questions.  
            - Make the interview experience **friendly and conversational**—introduce yourself, add small talk, or acknowledge the user's answers through the argument named `question_prompt` in the ask_interveiw_question_tool.
            - Always ask the pre-determined question first, then ask **at least 2 follow-up questions** to dive deeper.
            - Personalize the follow-up questions based on the user's response.
            - After collecting all responses, **handoff to submit_interview_agent**.  
            """,
        tools=tools,
        can_handoff_to=["submit_interview_agent"],
    )
    return conduct_interview_agent
