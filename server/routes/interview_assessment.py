from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
import logging
from classes.user_claims import UserClaims
from database.interview_assessment import InterviewAssessment
from utils.jwt import require_auth
from utils.responses import create_response

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/list")
async def get_interview_assessments(
    interview_uuid: str, user_claims: UserClaims = Depends(require_auth)
):
    try:
        assessments = await InterviewAssessment.find(
            InterviewAssessment.interview.uuid == UUID(interview_uuid),  # type:ignore
            InterviewAssessment.interview.organization.users.user._id  # type:ignore
            == user_claims.user.id,
            fetch_links=True,
            nesting_depths_per_field={"interview": 4},
        ).to_list()

        logger.debug(f"2ASSESSMENTS {assessments}")

        return create_response(
            success=True, data=[await a.to_public_dict() for a in assessments]
        )
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail=str(e))
