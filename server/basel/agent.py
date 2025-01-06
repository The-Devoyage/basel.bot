import logging
from typing import List, Optional
from beanie import SortDirection
from llama_index.agent.openai import OpenAIAgent
from llama_index.agent.openai.openai_assistant_agent import MessageRole
from llama_index.core.base.llms.types import ChatMessage
from llama_index.core.tools import BaseTool
from basel.get_system_prompt import get_system_prompt
from basel.tools import (
    get_admin_tools,
    get_candidate_tools,
    get_general_tools,
    get_global_tools,
    get_unauthenticated_tools,
)
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

    # Unauthenticated Tools
    tools.extend(get_unauthenticated_tools())

    # Authenticated Tools + Setup Agent
    if chatting_with and (
        (shareable_link and shareable_link.status) or not shareable_link
    ):
        tools: List[BaseTool] = get_global_tools(chatting_with)

        if user_claims:
            # Get Authenticated Tools
            # Handle Admin Role Tools
            role = await user_claims.user.role.fetch()
            if not role:
                raise Exception("Can't find role")

            if role.identifier == RoleIdentifier.ADMIN:  # type:ignore
                tools.extend(get_admin_tools())

            # Handle General User Role Tools
            tools.extend(get_general_tools(user_claims.user))

            # Tools for the candidate
            if chatting_with.id == user_claims.user.id:
                tools.extend(get_candidate_tools(user_claims.user, role))  # type:ignore

                # Populate Recent Chat History
                messages = (
                    await Message.find(
                        Message.user.id == user_claims.user.id  # type:ignore
                    )
                    .limit(20)
                    .sort(
                        [(Message.created_at, SortDirection.DESCENDING)]  # type:ignore
                    )
                    .to_list()
                )
                for message in messages:
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
