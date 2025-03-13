import logging
from typing import List, Optional, Tuple
from beanie import SortDirection
from llama_index.agent.openai.openai_assistant_agent import MessageRole
from llama_index.core.base.llms.types import ChatMessage
from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.core.workflow import Context
from basel.agents import aggregate_authenticated_agents, aggregate_public_agents
from classes.user_claims import UserClaims
from database.message import Message
from database.shareable_link import ShareableLink
from database.user import User

from utils.subscription import SubscriptionStatus

logger = logging.getLogger(__name__)


async def get_agent_workflow(
    is_current_user,
    chatting_with: Optional[User],
    user_claims: Optional[UserClaims],
    subscription_status: SubscriptionStatus,
    shareable_link: ShareableLink | None,
) -> Tuple[AgentWorkflow, List[ChatMessage]]:
    logger.debug(f"GETTING AGENT FOR USER {chatting_with}")

    chat_history: List[ChatMessage] = []

    # Authenticated Tools + Setup Agent
    if chatting_with and (
        (shareable_link and shareable_link.status) or not shareable_link
    ):
        if user_claims:
            # Get Authenticated Tools
            # Handle Admin Role Tools
            role = await user_claims.user.role.fetch()
            if not role:
                raise Exception("Can't find role")

            # Tools for the candidate
            if chatting_with.id == user_claims.user.id:
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
                    if not message.text:
                        continue
                    history = ChatMessage(
                        role=MessageRole.ASSISTANT
                        if message.sender == "bot"
                        else MessageRole.USER,
                        content=message.text + f"/n{message.context}"
                        if message.context
                        else message.text,
                    )
                    chat_history.append(history)
                chat_history.reverse()

    agents = aggregate_public_agents(
        chatting_with=chatting_with,
        shareable_link=shareable_link,
        user_claims=user_claims,
        is_candidate=is_current_user,
        subscription_status=subscription_status,
    )
    if user_claims and chatting_with:
        authenticated_agents = aggregate_authenticated_agents(
            chatting_with=chatting_with,
            is_current_user=is_current_user,
            subscription_status=subscription_status,
        )
        agents.extend(authenticated_agents)

    agent_workflow = AgentWorkflow(agents=agents, root_agent="root_agent")
    ctx = Context(agent_workflow)

    return (agent_workflow, chat_history)
