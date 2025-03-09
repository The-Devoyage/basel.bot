from functools import partial
from typing import Optional
from uuid import UUID
from beanie.operators import In
from chromadb.api.models.Collection import logging
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.bridge.pydantic import BaseModel, Field
from llama_index.core.tools.function_tool import FunctionTool
from llama_index.core.workflow import Context, HumanResponseEvent, InputRequiredEvent
from basel.tools.create_get_interview_question_response_tool import (
    create_get_interview_question_responses_tool,
)
from basel.tools.get_interview_questions_tool import create_get_interview_questions_tool
from database.interview import Interview
from database.interview_assessment import InterviewAssessment
from database.interview_question import InterviewQuestion
from database.interview_question_response import InterviewQuestionResponse

from database.user import User

logger = logging.getLogger(__name__)


class CreateInterviewAssessmentAgentParams(BaseModel):
    interview_uuid: UUID = Field(
        description="The UUID of the interview that the user has just taken."
    )


class CreateInterviewAssessmentParams(BaseModel):
    interview_uuid: UUID = Field(
        description="The UUID of the interview that the user has just taken."
    )
    overall: int = Field(
        description="""
            Overall Interview Performance Rating 1 - 5:
            A rating of 1 - 5 on how the user did overall in the interview.
            Consistency – Did the user maintain a strong performance throughout the interview?
            Professionalism – Was the user respectful and professional in their responses?
        """,
    )
    content_relevance: Optional[int] = Field(
        description="""
            Content and Relevance Rating 1 - 5:
            Answer Quality – How well the user's response answers the question.
            Relevance – Does the response stay on topic and address the question directly?
            Completeness – Does the answer provide sufficient detail for each question, or is it too vague?
            - Users should submit 4 or more sentenences for each response.
        """
    )
    communication_skills: Optional[int] = Field(
        description="""
        Communication Skills - Rating 1 - 5:
            Clarity – Is the response clear and understandable?
            Conciseness – Does the user get to the point without unnecessary filler?
            Use of Professional Language – Is the language appropriate for a professional setting?
        """
    )
    confidence_delivery: Optional[int] = Field(
        description="""
            Confidence & Delivery - Rating 1 - 5:
            Pacing – Was the response too rushed or too slow?
            Use of Filler Words – Does the user rely too much on "um," "like," or "you know"?
            Tone & Enthusiasm – Is the user engaging and confident?
        """
    )
    structure_organization: Optional[int] = Field(
        description="""
            Structure & Organization - Rating 1 - 5:
            Logical Flow – Does the response follow a structured and logical order?
            Use of Examples – Did the user support their answer with relevant examples?
            Coherence – Is the response easy to follow?
        """
    )
    adaptability_critical_thinking: Optional[int] = Field(
        description="""
            Adaptability & Critical Thinking - Rating 1 - 5:
            Handling Unexpected Questions – How well does the user respond to curveball questions?
            Problem-Solving Ability – Does the user demonstrate analytical skills when needed?
            Creativity – Does the response show unique or innovative thinking?
        """
    )
    technical_industry_knowledge: Optional[int] = Field(
        description="""
            Technical/Industry Knowledge (If Applicable) - Rating 1 - 5
            Accuracy – Are the answers factually correct?
            Depth of Knowledge – Does the user demonstrate expertise?
            Use of Terminology – Is industry-specific language used correctly?
        """
    )


async def create_interview_assessment(
    ctx: Context,
    user: User,
    interview_uuid: str,
    overall: int,
    content_relevance: Optional[int] = None,
    communication_skills: Optional[int] = None,
    confidence_delivery: Optional[int] = None,
    structure_organization: Optional[int] = None,
    adaptability_critical_thinking: Optional[int] = None,
    technical_industry_knowledge: Optional[int] = None,
):
    logger.debug("CREATING ASSESSMENT")
    ctx.write_event_to_stream(
        InputRequiredEvent(
            prefix="Are you sure you want to submit this for assessment? This can not be undone. You must type `yes` to approve.",
        )
    )
    logger.debug("WAITING FOR APPROVAL")

    response = await ctx.wait_for_event(HumanResponseEvent)
    logger.debug("APPROVAL")

    if response.response.lower() == "yes":
        logger.debug(f"RESPONSE APPROVED: {interview_uuid}")

        try:
            interview = await Interview.find_one(Interview.uuid == UUID(interview_uuid))

            if not interview:
                raise Exception(
                    "Failed to find the interview when creating final assessment."
                )

            assessment = await InterviewAssessment.find_one(
                InterviewAssessment.interview.id == interview.id,  # type:ignore
                InterviewAssessment.user.id == user.id,  # type:ignore
            )

            if assessment:
                raise Exception("The user has already submitted their assessment.")

            questions = await InterviewQuestion.find(
                InterviewQuestion.interview.id == interview.id  # type:ignore
            ).to_list()
            responses = await InterviewQuestionResponse.find(
                InterviewQuestionResponse.user.id == user.id,  # type:ignore
                In(
                    InterviewQuestionResponse.interview_question.id,  # type:ignore
                    [q.id for q in questions],
                ),
            ).count()

            if not questions or not responses or (len(questions) != responses):
                logger.error(f"QUESTIONS: {questions}; RESPONSES {responses}")
                raise Exception("User has not completed the interview.")

            interview_assessment = await InterviewAssessment(
                overall=overall,
                content_relevance=content_relevance,
                communication_skills=communication_skills,
                confidence_delivery=confidence_delivery,
                structure_organization=structure_organization,
                adaptability_critical_thinking=adaptability_critical_thinking,
                technical_industry_knowledge=technical_industry_knowledge,
                user=user,  # type:ignore
                created_by=user,  # type:ignore
                interview=interview,  # type:ignore
            ).create()
            return interview_assessment
        except Exception as e:
            logger.debug(f"CREATE ASSESMENT ERROR: {str(e)}")
            return str(e)
    else:
        logger.debug("ABORTED")
        return "Assessment Aborted"


# async def create_assessment_agent(ctx: Context, user: User, interview_uuid: str):
#     logger.debug("CREATING ASSESSMENT")
#     ctx.write_event_to_stream(
#         InputRequiredEvent(
#             prefix="Are you sure you want to submit this for assessment? This can not be undone. You must type `yes` to approve.",
#         )
#     )
#     logger.debug("WAITING FOR APPROVAL")

#     response = await ctx.wait_for_event(HumanResponseEvent)
#     logger.debug("APPROVAL")

#     if response.response.lower() == "yes":
#         logger.debug("RESPONSE APPROVED")
# interview_assessment_tool = FunctionTool.from_defaults(
#     name="interview_assessment_tool",
#     description="""
#         Useful to create and save an assessment for interview responses.
#     """,
#     async_fn=lambda interview_uuid, overall, content_relevance=None, communication_skills=None, confidence_delivery=None, structure_organization=None, adaptability_critical_thinking=None, technical_industry_knowledge=None: create_interview_assessment(
#         user=user,
#         interview_uuid=interview_uuid,
#         overall=overall,
#         content_relevance=content_relevance,
#         communication_skills=communication_skills,
#         confidence_delivery=confidence_delivery,
#         structure_organization=structure_organization,
#         adaptability_critical_thinking=adaptability_critical_thinking,
#         technical_industry_knowledge=technical_industry_knowledge,
#     ),
#     fn_schema=CreateInterviewAssessmentParams,
# )
# agent = OpenAIAgent.from_tools(
#     tools=[
#         interview_assessment_tool,
#         create_get_interview_questions_tool(),
#         create_get_interview_question_responses_tool(user),
#     ],
#     verbose=True,
#     system_prompt="""
#         - Your job is to assess the responses for an interview provided by the user.
#         - Assessments for each category range between 1 and 5.
#         - Assessments should be critical and rigorous and users that provide thorough well thought responses should receive high scores.
#     """,
# )
# response = await agent.aquery(
#     f"""
#         Create an assessment for the following interview uuid: {interview_uuid}.
#         1. First, Use the get_interview_questions tool to get the interview questions.
#         2. Then, Use the get_interview_question_responses tool to get the interview responses.
#         3. Finally, Use the create_interview_assessment tool to perform the assessment.
#     """
# )

# return response.response
# else:
#     logger.debug("ABORTED")
#     return "Assessment aborted."


def create_create_interview_assessment_tool(user: User):
    interview_assessment_agent_tool = FunctionTool.from_defaults(
        name="interview_assessment_tool",
        description="""
            - Used after a user completes or answers all questions in an interview.
            - Useful to mark an interview complete and share the results to the publisher of the interview.
            - Submits an interview to the organization if exists.
            - Never accept user submitted input for the assessment.
        """,
        async_fn=partial(create_interview_assessment, user=user),
        fn_schema=CreateInterviewAssessmentParams,
    )

    return interview_assessment_agent_tool
