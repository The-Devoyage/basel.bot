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
from basel.create_get_interview_question_response_tool import (
    create_get_interview_question_responses_tool,
)
from basel.create_interview_question_tool import create_create_interview_question_tool
from basel.create_interview_tool import create_create_interview_tool
from basel.get_interview_questions_tool import create_get_interview_questions_tool
from basel.get_interviews_tool import (
    create_get_interviews_tool,
)
from basel.get_system_prompt import get_system_prompt
from classes.user_claims import UserClaims
from database.role import RoleIdentifier
from database.message import Message
from database.shareable_link import ShareableLink
from database.user import User

from utils.subscription import SubscriptionStatus

logger = logging.getLogger(__name__)


async def get_agent(
    is_candidate,
    chatting_with: Optional[User],
    user_claims: Optional[UserClaims],
    subscription_status: SubscriptionStatus,
    shareable_link: ShareableLink | None,
) -> OpenAIAgent:
    logger.debug(f"GETTING AGENT FOR USER {chatting_with}")
    system_prompt = await get_system_prompt(
        subscription_status, user_claims, chatting_with, is_candidate, shareable_link
    )

    tools: List[BaseTool] = []
    chat_history: List[ChatMessage] = []

    # Get the About Basel Tool
    about_tool = create_about_tool()
    tools.append(about_tool)

    if chatting_with and (
        (shareable_link and shareable_link.status) or not shareable_link
    ):
        tools: List[BaseTool] = []

        # Global Tools
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

        if user_claims:
            # Get Authenticated Tools
            # Handle Admin Role Tools
            role = await user_claims.user.role.fetch()
            if not role:
                raise Exception("Can't find role")

            if role.identifier == RoleIdentifier.ADMIN:  # type:ignore
                create_interview_tool = create_create_interview_tool(user_claims.user)
                tools.append(create_interview_tool)

                create_interview_question_tool = create_create_interview_question_tool(
                    user_claims.user
                )
                tools.append(create_interview_question_tool)

            # Handle General User Role Tools
            create_interview_question_response = (
                create_create_interview_question_response_tool(user_claims.user)
            )
            tools.append(create_interview_question_response)

            # Populate Recent Chat History
            messages = (
                await Message.find(
                    Message.user.id == user_claims.user.id  # type:ignore
                )
                .limit(40)
                .to_list()
            )
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
