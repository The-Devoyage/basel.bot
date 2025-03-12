from typing import Optional
from llama_index.core.agent.workflow import FunctionAgent
from basel.get_system_prompt import get_system_prompt
from classes.user_claims import UserClaims
from database.shareable_link import ShareableLink
from database.user import User
from utils.subscription import SubscriptionStatus


def init_root_agent(
    subscription_status: SubscriptionStatus,
    user_claims: Optional[UserClaims],
    chatting_with: Optional[User],
    is_candidate: bool,
    shareable_link: Optional[ShareableLink],
):
    system_prompt = get_system_prompt(
        subscription_status=subscription_status,
        user_claims=user_claims,
        chatting_with=chatting_with,
        is_candidate=is_candidate,
        shareable_link=shareable_link,
    )
    root_agent = FunctionAgent(
        name="root_agent",
        description="An agent with access to tools for a user who has not authenticated.",
        system_prompt=system_prompt,
        can_handoff_to=[
            "conduct_interview_agent",
            "candidate_agent",
            "create_interview_agent",
            "manage_user_agent",
            "resume_generator_agent",
            "standup_agent",
            "update_interview_agent",
        ],
    )

    return root_agent
