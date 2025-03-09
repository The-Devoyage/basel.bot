from llama_index.core.agent.workflow import FunctionAgent

from basel.tools.create_insert_user_meta_tool import create_insert_user_meta_tool
from basel.tools.create_update_user_tool import create_update_user_tool
from database.user import User


def init_manage_user_agent(current_user: User):
    tools = []

    # Create Meta Tool
    insert_user_meta_tool = create_insert_user_meta_tool(current_user)
    tools.append(insert_user_meta_tool)

    # Update User
    update_user_tool = create_update_user_tool(current_user)
    tools.append(update_user_tool)

    manage_user_agent = FunctionAgent(
        name="manage_user_agent",
        description="Useful for saving new profile information about the current user.",
        system_prompt="""
            You are the `manage_user_agent` that can save user profile information including identity information and memories about the users career.
            - When a user mentions skills, career facts, hobbies, or personal interests, log the information using the `insert_user_meta_tool`.  
            - When a user provides profile details (e.g., first name, last name), update their information using the `update_user_tool`.          
        """,
        tools=tools,
    )
    return manage_user_agent
