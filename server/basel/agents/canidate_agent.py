from llama_index.core.agent.workflow import FunctionAgent
from basel.tools.candidate_profile_tool import create_candidate_profile_tool
from database.user import User


def init_candidate_agent(chatting_with: User):
    canidate_profile_tool = create_candidate_profile_tool(chatting_with)
    canidate_agent = FunctionAgent(
        name="canidate_agent",
        description="Useful for getting information about the canidate",
        system_prompt="""
            - You are an agent with access to stored memories about a candidate's work history, goals, hobbies, and other profile-related details.  
            - Use the `candidate_profile_tool` to retrieve the information about the candidate.
            - Retrieve and provide the most relevant information based on the request. If the request is too broad, ask for clarification.  
            - Once you find the necessary details, return the information to the requesting agent.  
        """,
        tools=[canidate_profile_tool],
    )
    return canidate_agent
