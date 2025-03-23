from llama_index.core.agent.workflow import FunctionAgent
from basel.tools.ask_interview_question_tool import init_ask_interview_question_tool
from basel.tools.get_interview_questions_tool import create_get_interview_questions_tool
from basel.tools.get_interviews_tool import create_get_interviews_tool
from basel.tools.pause_conduct_interview_tool import init_pause_conduct_interview_tool
from basel.tools.start_conduct_interview_tool import init_start_conduct_interview_tool

from database.user import User


def init_conduct_interview_agent(current_user: User):
    tools = []

    get_interview_questions_tool = create_get_interview_questions_tool()
    tools.append(get_interview_questions_tool)

    get_interviews_tool = create_get_interviews_tool()
    tools.append(get_interviews_tool)

    # Ask interview question tool
    ask_interview_question_tool = init_ask_interview_question_tool(current_user)
    tools.append(ask_interview_question_tool)

    # Pause Conduct Interview Tool
    pause_conduct_interview_tool = init_pause_conduct_interview_tool()
    tools.append(pause_conduct_interview_tool)

    # Start Conduct Interview Tool
    start_conduct_interview_tool = init_start_conduct_interview_tool(current_user)
    tools.append(start_conduct_interview_tool)

    conduct_interview_agent = FunctionAgent(
        name="conduct_interview_agent",
        description="Useful for conducting an interviews.",
        system_prompt="""
            You are the conduct_interview_agent that conducts interviews by asking interview questions to the user.  
            - Always initiate the `start_conduct_interview_tool` to begin the interview when this agent is called.
            - Use the `get_interview_questions_tool` to get the pre-determined questions to ask.
            - Always use the `ask_interview_question_tool` to interact with the user.  
            - Make the interview experience **friendly and conversational**—introduce yourself, add small talk, or acknowledge the user's answers through the argument named `question_prompt` in the ask_interveiw_question_tool.
            - Always ask the pre-determined question first, then ask **at least 2 and at most 4 follow-up questions** to dive deeper.
            - Personalize the follow-up questions based on the user's response.
            - After collecting all responses, **handoff to submit_interview_agent**.  
            - If the user wants to pause the interivew and pick up later, use the `pause_conduct_interview_tool`.
            - Never ask interview questions without utilizing the `ask_interview_question_tool`
            """,
        tools=tools,
        can_handoff_to=["submit_interview_agent"],
    )
    return conduct_interview_agent
