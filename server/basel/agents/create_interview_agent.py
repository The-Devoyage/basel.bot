from llama_index.core.agent.workflow import FunctionAgent

from basel.tools import scrape_webpage_tool
from basel.tools.create_interview_question_tool import (
    create_create_interview_question_tool,
)
from basel.tools.create_interview_tool import create_create_interview_tool
from database.user import User
from utils.subscription import SubscriptionStatus


def init_create_interview_agent(
    current_user: User, subscription_status: SubscriptionStatus
):
    tools = []

    # Create Interview Tool
    create_interview_tool = create_create_interview_tool(
        current_user, subscription_status
    )
    tools.append(create_interview_tool)

    # Create Interview Question Tool
    create_interview_question_tool = create_create_interview_question_tool(current_user)
    tools.append(create_interview_question_tool)

    # Scrape webpage tool
    # tools.append(scrape_webpage_tool)

    create_interview_agent = FunctionAgent(
        name="create_interview_agent",
        description="Useful to create an interview for a new job posting.",
        system_prompt=(
            "You are the create_interview_agent that can create interviews for new job postings on the Basel Platform."
            "You should always request the URL to the job posting before creating the interview."
            "You should always scrape the posting's web page with the `scrape_webpage_tool` to learn about the posting."
            "You should aways add questions when creating a new interview."
        ),
        tools=tools,
    )
    return create_interview_agent
