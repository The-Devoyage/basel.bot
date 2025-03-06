from llama_index.core.agent.workflow import FunctionAgent

from basel.tools.get_interview_questions_tool import create_get_interview_questions_tool
from basel.tools.get_interviews_tool import create_get_interviews_tool


def init_interview_retriever_agent():
    tools = []

    get_interview_questions_tool = create_get_interview_questions_tool()
    tools.append(get_interview_questions_tool)

    get_interviews_tool = create_get_interviews_tool()
    tools.append(get_interviews_tool)

    agent = FunctionAgent(
        name="interview_retriever_agent",
        description="Useful to lookup interviews and interview questions from the database.",
        system_prompt="""
            You are the Interview Retriever Agent that can query the database for interviews and/or the questions belonging to an interview.
        """,
        tools=tools,
    )

    return agent
