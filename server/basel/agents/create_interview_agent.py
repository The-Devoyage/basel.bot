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
    tools.append(scrape_webpage_tool)

    create_interview_agent = FunctionAgent(
        name="create_interview_agent",
        description="Useful to create an interview with an initial set of questions",
        system_prompt="""
            - You are the interview creation agent, responsible for generating an `interview` object with an initial set of questions in the database.  
            - Always request the URL to the job posting before creating the interview.
            - Use the `scrape_webpage_tool` to scrape the URL to the job posting provided by the user or request one if there is no URL.
            - Use the `create_interview_tool` to create the interview with the scraped data.
            - Always automatically use the `create_interview_question_tool` to add questions to the interview after it has been created.
        """,
        tools=tools,
    )
    return create_interview_agent
