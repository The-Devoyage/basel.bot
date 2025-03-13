from llama_index.core.agent.workflow import FunctionAgent
from basel.tools.create_create_interview_assessment_tool import (
    create_create_interview_assessment_tool,
)
from database.user import User


def init_submit_interview_agent(current_user: User):
    tools = []

    # Create interview assessment tool
    create_interview_assessment_tool = create_create_interview_assessment_tool(
        user=current_user
    )
    tools.append(create_interview_assessment_tool)

    submit_interview_agent = FunctionAgent(
        name="submit_interview_agent",
        description="Useful for submiting an interview.",
        system_prompt="""
            You are the submit_interview_agent that can submit and assess interviews for candidates. 
            - Call the `get_interview_questions_tool` to fetch the questions associated with an interview.
            - Call the `get_interview_question_responses_tool` to fetch user responses to interview questions.
            - If all questions are not answered, hand off to the `conduct_interview_agent` to finish interview.
            - Call the `create_interview_assessment_tool` to assess and submit the interview.
        """,
        tools=tools,
        can_handoff_to=["conduct_interview_agent"],
    )
    return submit_interview_agent
