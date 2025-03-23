from llama_index.core.agent.workflow import FunctionAgent

from basel.tools.get_interview_questions_tool import create_get_interview_questions_tool
from basel.tools.get_interviews_tool import create_get_interviews_tool


def init_interview_agent():
    tools = []

    get_interview_questions_tool = create_get_interview_questions_tool()
    tools.append(get_interview_questions_tool)

    get_interviews_tool = create_get_interviews_tool()
    tools.append(get_interviews_tool)

    agent = FunctionAgent(
        name="interview_retriever_agent",
        description="Useful to conduct, create, and update interviews.",
        system_prompt="""
            - You are the Interview Agent responsible to fetch the interview details and handoff to the correct agent based on task..

            - Always try to use the `get_interview_tool` to get interview details.
            - Always try to use the `get_interview_questions_tool` to get the questions associated with an interview.

            **Hand Off**
            - To conduct interviews, hand off the task to the `conduct_interview_agent`.
            - To create a new interview, hand off the task to the `create_interview_agent`.
            - To update an interview, hand off the task to the `update_interview_agent`.
        """,
        tools=tools,
        can_handoff_to=[
            "conduct_interview_agent",
            "create_interview_agent",
            "update_interview_agent",
        ],
    )

    return agent
