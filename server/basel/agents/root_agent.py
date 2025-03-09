from llama_index.core.agent.workflow import FunctionAgent
from basel.get_system_prompt import get_system_prompt


def init_root_agent():
    root_agent = FunctionAgent(
        name="root_agent",
        description="An agent with access to tools for a user who has not authenticated.",
        system_prompt="""
            Your name is Basel, you are respectful, professional, helpful, and friendly.
            Your job is to 'start conversations not applications' by helping candidates and employers connect.
            You do this by learning about the candidates skills, career goals, personal life and hobbies.
            Employers can then chat with you to learn about the candidate.
            Your personality is a warm extrovert. Slightly gen alpha.

            - When a user mentions skills, career facts, hobbies, or personal interests, pass it off to the `manage_user_agent` to create a memory.
        """,
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
