from chromadb.api.models.Collection import logging
from fastapi import APIRouter, Depends, HTTPException
from database.interview_assessment import InterviewAssessment
from database.user_meta import UserMeta
from database.shareable_link import ShareableLink

from classes.user_claims import UserClaims
from utils.jwt import require_auth
from utils.responses import create_response


router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/onboarding")
async def get_onboarding(
    user_claims: UserClaims = Depends(require_auth),
):
    try:
        metas = await UserMeta.find(
            UserMeta.user.id == user_claims.user.id  # type:ignore
        ).count()
        links = await ShareableLink.find(
            ShareableLink.user.id == user_claims.user.id  # type:ignore
        ).to_list()
        views = 0
        for link in links:
            views += link.views
        assessments = await InterviewAssessment.find(
            InterviewAssessment.user.id == user_claims.user.id  # type:ignore
        ).count()
        onboard_progress = {
            "metas": metas > 0,
            "interviews": assessments > 0,
            "links": len(links) > 0,
            "views": views > 0,
        }
        return create_response(success=True, data=onboard_progress)

    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")
