from basel.agents.canidate_agent import init_candidate_agent
from basel.agents.create_interview_agent import init_create_interview_agent
from basel.agents.interview_retriever import init_interview_retriever_agent
from basel.agents.manager_user_agent import init_manage_user_agent
from basel.agents.resume_agent import init_resume_generator_agent
from basel.agents.root_agent import init_root_agent
from basel.agents.standup_agent import init_standup_agent
from database.user import User
from utils.subscription import SubscriptionStatus


def aggregate_public_agents():
    agents = []

    # Root Agent
    root_agent = init_root_agent()
    agents.append(root_agent)

    # Get Interviews and Questions
    interview_retriever = init_interview_retriever_agent()
    agents.append(interview_retriever)

    return agents


def aggregate_authenticated_agents(
    chatting_with: User,
    subscription_status: SubscriptionStatus,
    is_current_user: bool = False,
):
    agents = []

    # Canidate Agent
    canidate_agent = init_candidate_agent(chatting_with)
    agents.append(canidate_agent)

    # Resume Generator Agent
    resume_generator_agent = init_resume_generator_agent()
    agents.append(resume_generator_agent)

    # Candidate only agents
    if is_current_user:
        # Manage user agent
        manage_user_agent = init_manage_user_agent(chatting_with)
        agents.append(manage_user_agent)
        # Standup Agent
        standup_agent = init_standup_agent(chatting_with, subscription_status)
        agents.append(standup_agent)

        # Create Interview Agent
        create_interview_agent = init_create_interview_agent(
            chatting_with, subscription_status
        )
        agents.append(create_interview_agent)

    return agents
