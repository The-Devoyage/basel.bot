from typing import Optional

from basel.agents.candidate_agent import init_candidate_agent
from basel.agents.conduct_interview_agent import init_conduct_interview_agent
from basel.agents.create_interview_agent import init_create_interview_agent
from basel.agents.interview_agent import init_interview_agent
from basel.agents.manage_user_agent import init_manage_user_agent
from basel.agents.resume_agent import init_resume_generator_agent
from basel.agents.root_agent import init_root_agent
from basel.agents.standup_agent import init_standup_agent
from basel.agents.submit_interview_agent import init_submit_interview_agent
from basel.agents.update_interview_agent import init_update_interview_agent
from classes.user_claims import UserClaims
from database.shareable_link import ShareableLink
from database.user import User
from utils.subscription import SubscriptionStatus


def aggregate_public_agents(
    chatting_with: Optional[User],
    subscription_status: SubscriptionStatus,
    is_candidate: bool,
    user_claims: Optional[UserClaims],
    shareable_link: Optional[ShareableLink],
):
    agents = []

    # Root Agent
    root_agent = init_root_agent(
        chatting_with=chatting_with,
        is_current_user=is_candidate,
        subscription_status=subscription_status,
        shareable_link=shareable_link,
        user_claims=user_claims,
    )
    agents.append(root_agent)

    # Get Interviews and Questions
    interview_agent = init_interview_agent()
    agents.append(interview_agent)

    if (shareable_link or user_claims) and chatting_with:
        # Canidate Agent
        canidate_agent = init_candidate_agent(chatting_with)
        agents.append(canidate_agent)
        # Resume Generator Agent
        resume_generator_agent = init_resume_generator_agent()
        agents.append(resume_generator_agent)

    return agents


def aggregate_authenticated_agents(
    chatting_with: User,
    subscription_status: SubscriptionStatus,
    is_current_user: bool = False,
):
    agents = []

    # Candidate only agents
    if is_current_user:
        # Manage user agent
        manage_user_agent = init_manage_user_agent(
            current_user=chatting_with, subscription_status=subscription_status
        )
        agents.append(manage_user_agent)

        # Standup Agent
        standup_agent = init_standup_agent(chatting_with, subscription_status)
        agents.append(standup_agent)

        # Create Interview Agent
        create_interview_agent = init_create_interview_agent(
            chatting_with, subscription_status
        )
        agents.append(create_interview_agent)

        # Update Interview Agent
        update_interview_agent = init_update_interview_agent(current_user=chatting_with)
        agents.append(update_interview_agent)

        # Conduct Interview Agent
        conduct_interview_agent = init_conduct_interview_agent(
            current_user=chatting_with
        )
        agents.append(conduct_interview_agent)

        # Submit Interview Agent
        submit_interview_agent = init_submit_interview_agent(current_user=chatting_with)
        agents.append(submit_interview_agent)

    return agents
