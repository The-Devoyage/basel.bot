from llama_index.core.agent.workflow import FunctionAgent

from basel.tools.create_resume_tool import create_create_resume_tool


def init_resume_generator_agent():
    create_resume_tool = create_create_resume_tool()
    resume_generator_agent = FunctionAgent(
        name="resume_generator_agent",
        description="Useful to generate a dynamic resume based on candidate's profile.",
        system_prompt="""
            You are the `resume_generator_agent` that can generate dynamic resumes to share with the candidate or recruiter.
            - You are responsible for creating a complete resume for a candidate based on their profile details.  
            - First, request any missing information from the `candidate_agent`. Call the agent for each section of information you need to request.
            - Then, use the available tools to generate a polished resume suitable for sharing with potential employers and recruiters.  
            - Only include verified details—avoid placeholders or assumptions.  
        """,
        tools=[create_resume_tool],
        can_handoff_to=[
            "candidate_agent",
        ],
    )
    return resume_generator_agent
