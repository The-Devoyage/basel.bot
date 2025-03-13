from functools import partial
from typing import Optional
from chromadb.api.models.Collection import logging
from llama_index.core.bridge.pydantic import BaseModel, Field
from llama_index.core.tools.function_tool import FunctionTool
from llama_index.core.workflow import Context, HumanResponseEvent, InputRequiredEvent
from database.interview import Interview
from database.interview_assessment import InterviewAssessment

from database.user import User

logger = logging.getLogger(__name__)


class CreateInterviewAssessmentParams(BaseModel):
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
    overall: int,
    content_relevance: Optional[int] = None,
    communication_skills: Optional[int] = None,
    confidence_delivery: Optional[int] = None,
    structure_organization: Optional[int] = None,
    adaptability_critical_thinking: Optional[int] = None,
    technical_industry_knowledge: Optional[int] = None,
):
    logger.debug("CREATING ASSESSMENT")

    pending_create_confirmation = await ctx.get("pending_create_response", False)

    current_interview_uuid = await ctx.get("current_interview_uuid", None)
    interview_in_progress = await ctx.get("interview_in_progress", False)
    if not current_interview_uuid or not interview_in_progress:
        return "Interview is not in progress. Use the `start_conduct_interview_tool` to start the interview."

    # Confirm
    if not pending_create_confirmation:
        await ctx.set("pending_create_response", True)
        ctx.write_event_to_stream(
            InputRequiredEvent(
                prefix="It looks like you are done with the interview. Do you want to submit this for assessment? This can not be undone. Type `yes` to approve.",
            )
        )

    response = await ctx.wait_for_event(HumanResponseEvent)

    # Finish Assessment
    await ctx.set("pending_create_confirmation", False)

    if response.response.lower() == "yes":
        try:
            interview = await Interview.find_one(
                Interview.uuid == current_interview_uuid
            )

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

            await ctx.set("current_interview_uuid", None)
            await ctx.set("interview_in_progress", False)

            return interview_assessment
        except Exception as e:
            logger.debug(f"CREATE ASSESMENT ERROR: {str(e)}")
            return "Something went wrong. Ask user if they want to try to submit the interview again."
    else:
        logger.debug("ABORTED")
        return f"The user has decided to keep the interview process going. Use the `ask_interview_question_tool` to contineu the process. User Message: {response.response}"


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
