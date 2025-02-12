from uuid import UUID
from chromadb.api.models.Collection import logging
from fastapi import APIRouter, HTTPException

from database.interview_question import InterviewQuestion
from utils.responses import create_response


router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/list")
async def get_interview_questions(interview_uuid: str):
    try:
        logger.debug("HMM")
        interview_questions = await InterviewQuestion.find(
            InterviewQuestion.interview.uuid == UUID(interview_uuid),  # type:ignore
            fetch_links=True,
        ).to_list()

        logger.debug(f"fetched questions: {interview_questions}")

        return create_response(
            success=True, data=[await q.to_public_dict() for q in interview_questions]
        )
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")
