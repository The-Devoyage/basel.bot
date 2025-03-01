import logging
from uuid import UUID
from beanie.operators import Set
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from classes.user_claims import UserClaims
from database.interview_assessment import InterviewAssessment
from database.interview_question import InterviewQuestion
from database.interview_question_response import InterviewQuestionResponse
from utils.jwt import require_auth
from utils.responses import create_response

logger = logging.getLogger(__name__)

router = APIRouter()


class UpsertInterviewQuestionResponseParams(BaseModel):
    response: str


@router.post("/upsert/{interview_question_uuid}")
async def upsert_interview_question_response(
    params: UpsertInterviewQuestionResponseParams,
    interview_question_uuid: str,
    user_claims: UserClaims = Depends(require_auth),
):
    try:
        interview_question = await InterviewQuestion.find_one(
            InterviewQuestion.uuid == UUID(interview_question_uuid), fetch_links=True
        )

        if not interview_question:
            raise Exception("Interview question not found.")

        interview_assessment = await InterviewAssessment.find_one(
            InterviewAssessment.interview.id  # type:ignore
            == interview_question.interview.id,  # type:ignore
            InterviewAssessment.user.id == user_claims.user.id,  # type:ignore
        )

        if interview_assessment:
            raise Exception("Interview already submitted. Editing is now disabled.")

        updated = await InterviewQuestionResponse.find_one(
            InterviewQuestionResponse.user.id == user_claims.user.id,  # type:ignore
            InterviewQuestionResponse.interview_question.id  # type:ignore
            == interview_question.id,
        ).upsert(
            Set({"response": params.response}),
            on_insert=InterviewQuestionResponse(
                user=user_claims.user,  # type:ignore
                interview_question=interview_question,  # type:ignore
                created_by=user_claims.user,  # type:ignore
                response=params.response,
            ),
        )

        # Handle Errors
        if not updated:
            raise Exception("Failed to upsert interview question response.")

        interview_question_response = await InterviewQuestionResponse.find_one(
            InterviewQuestionResponse.user.id == user_claims.user.id,  # type:ignore
            InterviewQuestionResponse.interview_question.id  # type:ignore
            == interview_question.id,
        )

        if not interview_question_response:
            raise Exception("Failed to find interview question response.")

        return create_response(
            success=True, data=await interview_question_response.to_public_dict()
        )
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail={str(e)})
