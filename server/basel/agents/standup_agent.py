from llama_index.core.agent.workflow import FunctionAgent

from basel.tools.create_create_standup_tool import create_create_standup_tool
from basel.tools.create_get_standups_tool import create_get_standups_tool
from database.user import User
from utils.subscription import SubscriptionStatus


def init_standup_agent(current_user: User, subscription_status: SubscriptionStatus):
    tools = []

    # Create Standup Tool
    create_standup_tool = create_create_standup_tool(current_user, subscription_status)
    tools.append(create_standup_tool)

    # Get Standups Tool
    get_standups_tool = create_get_standups_tool(current_user)
    tools.append(get_standups_tool)
    standup_agent = FunctionAgent(
        name="standup_agent",
        description="Useful to fetch or log standups.",
        system_prompt="""
            - You are the standup agent, assisting users with logging standups, recalling past standups, and expanding conversations to learn more about the candidate.  
            - Use the create_standup_tool to save the user standup to the database.
            - Use standup details to help users track progress and stay aligned with their goals.  
            - After logging a standup, engage the user in a conversation about their goals to encourage reflection and progress.
        """,
        tools=tools,
    )
    return standup_agent
