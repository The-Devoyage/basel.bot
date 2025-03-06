from basel.agents.canidate_agent import init_candidate_agent
from basel.agents.interview_retriever import init_interview_retriever_agent
from basel.agents.manager_user_agent import init_manage_user_agent
from basel.agents.resume_agent import init_resume_generator_agent
from basel.agents.root_agent import init_root_agent
from database.user import User


def aggregate_public_agents():
    agents = []

    # Root Agent
    root_agent = init_root_agent()
    agents.append(root_agent)

    # Get Interviews and Questions
    interview_retriever = init_interview_retriever_agent()
    agents.append(interview_retriever)

    return agents


def aggregate_authenticated_agents(chatting_with: User, is_candidate: bool = False):
    agents = []

    # Canidate Agent
    canidate_agent = init_candidate_agent(chatting_with)
    agents.append(canidate_agent)

    # Resume Generator Agent
    resume_generator_agent = init_resume_generator_agent()
    agents.append(resume_generator_agent)

    # Candidate only agents
    if is_candidate:
        # Manage user agent
        manage_user_agent = init_manage_user_agent(chatting_with)
        agents.append(manage_user_agent)

    return agents
