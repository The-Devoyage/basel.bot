import logging
from typing import List, Optional
from llama_index.agent.openai import OpenAIAgent
from llama_index.agent.openai.openai_assistant_agent import MessageRole
from llama_index.core.base.llms.types import ChatMessage
from llama_index.core.tools import BaseTool
from basel.candidate_profile_tool import create_candidate_profile_tool
from basel.create_about_tool import create_about_tool
from basel.create_create_interview_question_response_tool import (
    create_create_interview_question_response_tool,
)
from basel.create_interview_question_tool import create_create_interview_question_tool
from basel.create_interview_tool import create_create_interview_tool
from basel.get_interview_questions_tool import create_get_interview_questions_tool
from basel.get_interviews_tool import (
    create_get_interviews_tool,
)
from basel.get_system_prompt import get_system_prompt
from classes.role import RoleIdentifier
from classes.user import User
from classes.user_claims import UserClaims
from database.message import MessageModel

from utils.subscription import SubscriptionStatus

logger = logging.getLogger(__name__)

message_model = MessageModel("basel.db")


def get_agent(
    is_candidate,
    chatting_with: Optional[User],
    user_claims: Optional[UserClaims],
    subscription_status: SubscriptionStatus,
) -> OpenAIAgent:
    logger.debug(f"GETTING AGENT FOR USER {chatting_with}")
    system_prompt = get_system_prompt(
        subscription_status, user_claims, chatting_with, is_candidate
    )

    tools: List[BaseTool] = []
    chat_history: List[ChatMessage] = []

    # Get the About Basel Tool
    about_tool = create_about_tool()
    tools.append(about_tool)

    if chatting_with:
        candidate_profile_tool = create_candidate_profile_tool(chatting_with.id)
        # Get Tools
        tools: List[BaseTool] = [candidate_profile_tool]

        if user_claims:
            # Get Authenticated Tools
            # Handle Admin Role Tools
            if user_claims.role.identifier == RoleIdentifier.ADMIN:
                logger.debug("HEYHEYHEY")
                create_interview_tool = create_create_interview_tool(
                    user_claims.user.id
                )
                tools.append(create_interview_tool)

                create_interview_question_tool = create_create_interview_question_tool(
                    user_claims.user.id
                )
                tools.append(create_interview_question_tool)

            # Handle General User Role Tools
            get_interviews_tool = create_get_interviews_tool()
            tools.append(get_interviews_tool)

            get_interview_questions_tool = create_get_interview_questions_tool()
            tools.append(get_interview_questions_tool)

            create_interview_question_response = (
                create_create_interview_question_response_tool(user_claims.user.id)
            )
            tools.append(create_interview_question_response)

            # Populate Recent Chat History
            conn = message_model._get_connection()
            cursor = conn.cursor()
            messages = message_model.get_messages(cursor, user_claims.user.id, limit=40)
            for message in messages:
                logger.debug(f"MESSAGE: {message}")
                history = ChatMessage(
                    role=MessageRole.ASSISTANT
                    if message.sender == "bot"
                    else MessageRole.USER,
                    content=message.text,
                )
                chat_history.append(history)

    agent = OpenAIAgent.from_tools(
        tools=tools,
        verbose=True,
        system_prompt=system_prompt,
        chat_history=chat_history,
    )
    return agent
