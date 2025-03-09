from llama_index.core.agent.workflow import FunctionAgent
from basel.tools.create_interview_question_tool import (
    create_create_interview_question_tool,
)

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

    # # Create Interview Question Tool
    create_interview_question_tool = create_create_interview_question_tool(current_user)
    tools.append(create_interview_question_tool)

    # Update Interview Question Tool
    update_interview_question_tool = create_update_interview_question_tool(current_user)
    tools.append(update_interview_question_tool)

    update_interview_agent = FunctionAgent(
        name="update_interview_agent",
        description="Useful for updating an interview or questions associated with an interview.",
        system_prompt="""
            You are the Update Interview Agent. You can update high level details of an interview
            or update the Questions belonging to the interview. You do not have the power to update user
            responses to questions.

            **Instructions**
            Use the `interview_retriever_agent` to fetch the interview.
            Use the `update_interview_tool` to update high level details of an interview such as `name`, `description`, or `status` (If the interview is enabled or disabeld).
            Use the `update_interview_question_tool` to update specific questions or the status of questions associated with an interview.
            Use the `create_interview_question_tool` to add new questions to an existing interview.
        """,
        tools=tools,
    )

    return update_interview_agent
