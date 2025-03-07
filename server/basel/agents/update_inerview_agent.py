from llama_index.core.agent.workflow import FunctionAgent
from basel.tools.create_update_interview_tool import create_update_interview_tool

from basel.tools.create_update_interviw_question_tool import (
    create_update_interview_question_tool,
)
from database.user import User


def init_update_interview_agent(current_user: User):
    tools = []

    # Update Interview Tool
    update_interview_tool = create_update_interview_tool(current_user)
    tools.append(update_interview_tool)

    # Update Interview Question Tool
    update_interview_question_tool = create_update_interview_question_tool(current_user)
    tools.append(update_interview_question_tool)

    update_interview_agent = FunctionAgent(
        name="update_interview_agent",
        description="Useful for updating high level details about an interview.",
        system_prompt="""
            - You are the update interview agent allowing users to update high level details about
            interviews.
            - Use the `update_interview_tool` to update details about the high level interview details.
            - User the `update_interview_question_tool` to update a question associated with an interview.
        """,
        tools=tools,
    )
    return update_interview_agent
