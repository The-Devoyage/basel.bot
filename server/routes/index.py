from datetime import datetime
import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from llama_index.core.bridge.pydantic import BaseModel
from basel.indexing import add_index, get_documents, reset_index
from classes.user_claims import UserClaims
from utils.jwt import require_auth

from utils.responses import create_response

router = APIRouter()

logger = logging.getLogger(__name__)


class PostIndexBody(BaseModel):
    chat_start_time: Optional[datetime] = None


@router.post("/reset-index")
async def index(body: PostIndexBody, user_claims: UserClaims = Depends(require_auth)):
    try:
        if not user_claims or not user_claims.user.id:
            raise Exception("Login Required.")
        documents = get_documents(user_claims.user, body.chat_start_time)
        reset_index(user_claims.user.id)
        add_index(documents, "user_meta")
        return create_response(success=True)
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500)
