from llama_index.core.agent.workflow import FunctionAgent
from basel.tools.candidate_profile_tool import init_candidate_profile_tool
from basel.tools.get_candidate_interviews import init_get_candidate_interviews_tool
from basel.tools.get_interview_assessment import init_get_interview_assessment_tool
from basel.tools.get_interview_transcript import init_get_interview_transcript_tool
from database.user import User


def init_candidate_agent(chatting_with: User):
    tools = []

    # Candidate Profile Tool
    canidate_profile_tool = init_candidate_profile_tool(chatting_with)
    tools.append(canidate_profile_tool)

    # Candidate Interviews Tool
    get_candidate_interviews_tool = init_get_candidate_interviews_tool(chatting_with)
    tools.append(get_candidate_interviews_tool)

    # Interview Transcripts
    get_interview_transcript_tool = init_get_interview_transcript_tool(chatting_with)
    tools.append(get_interview_transcript_tool)

    # Interview Assessment
    get_interview_assessment_tool = init_get_interview_assessment_tool(chatting_with)
    tools.append(get_interview_assessment_tool)

    canidate_agent = FunctionAgent(
        name="candidate_agent",
        description="Useful for retrieving details about the canidate and their career/interviews they have taken.",
        system_prompt="""
            - You are the candidate_agent that can answer questions and provide details about the candidate.  
            - Use the `candidate_profile_tool` to retrieve saved memories about the candidate.
            - Use the `get_candidate_interviews_tool` to retrieve interviews the candidate has taken.
        """,
        tools=tools,
        can_handoff_to=[],
    )
    return canidate_agent
