from typing import List
from llama_index.core.tools import BaseTool
from basel.tools.candidate_profile_tool import create_candidate_profile_tool
from basel.tools.create_about_tool import create_about_tool
from basel.tools.create_create_interview_question_response_tool import (
    create_create_interview_question_response_tool,
)
from basel.tools.create_create_standup_tool import create_create_standup_tool
from basel.tools.create_get_interview_question_response_tool import (
    create_get_interview_question_responses_tool,
)
from basel.tools.create_get_standups_tool import create_get_standups_tool
from basel.tools.create_interview_question_tool import (
    create_create_interview_question_tool,
)
from basel.tools.create_interview_tool import create_create_interview_tool
from basel.tools.create_update_interviw_question_tool import (
    create_update_interview_question_tool,
)
from basel.tools.create_update_user_tool import create_update_user_tool
from basel.tools.get_interview_questions_tool import create_get_interview_questions_tool
from basel.tools.get_interviews_tool import create_get_interviews_tool
from basel.tools.scrape_webpage_tool import scrape_webpage_tool
from basel.tools.create_insert_user_meta_tool import create_insert_user_meta_tool
from basel.tools.create_update_interview_tool import create_update_interview_tool

# DB
from database.user import User


def get_unauthenticated_tools():
    tools: List[BaseTool] = []

    about_tool = create_about_tool()
    tools.append(about_tool)

    return tools


def get_global_tools(chatting_with: User):
    tools: List[BaseTool] = []

    candidate_profile_tool = create_candidate_profile_tool(chatting_with)
    tools.append(candidate_profile_tool)

    get_interview_question_responses_tool = (
        create_get_interview_question_responses_tool(chatting_with)
    )
    tools.append(get_interview_question_responses_tool)

    get_interview_questions_tool = create_get_interview_questions_tool()
    tools.append(get_interview_questions_tool)

    get_interviews_tool = create_get_interviews_tool()
    tools.append(get_interviews_tool)

    return tools


def get_admin_tools(current_user: User):
    tools: List[BaseTool] = []

    # Scrape Webpage Tool
    tools.append(scrape_webpage_tool)

    # Create Interview Tool
    create_interview_tool = create_create_interview_tool(current_user)
    tools.append(create_interview_tool)

    # Update Interview Tool
    update_interview_tool = create_update_interview_tool(current_user)
    tools.append(update_interview_tool)

    # Create Interview Question Tool
    create_interview_question_tool = create_create_interview_question_tool(current_user)
    tools.append(create_interview_question_tool)

    # Update Interview Question Tool
    update_interview_question_tool = create_update_interview_question_tool()
    tools.append(update_interview_question_tool)

    return tools


def get_general_tools(current_user: User):
    tools: List[BaseTool] = []

    # Create Interview Question Response Tool
    create_interview_question_response = create_create_interview_question_response_tool(
        current_user
    )
    tools.append(create_interview_question_response)

    return tools


def get_candidate_tools(current_user: User):
    tools: List[BaseTool] = []
    # Update User
    update_user_tool = create_update_user_tool(current_user)
    tools.append(update_user_tool)

    # Create Standup Tool
    create_standup_tool = create_create_standup_tool(current_user)
    tools.append(create_standup_tool)

    # Get Standups Tool
    get_standups_tool = create_get_standups_tool(current_user)
    tools.append(get_standups_tool)

    # Create meta tool
    insert_user_meta_tool = create_insert_user_meta_tool(current_user)
    tools.append(insert_user_meta_tool)

    return tools
