import logging
from fastapi import APIRouter
from fastapi.param_functions import Depends
from classes.user_claims import UserClaims
from database.role import Role

from utils.jwt import require_auth
from utils.responses import create_response

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/roles")
async def roles(_: UserClaims = Depends(require_auth)):
    roles = await Role.find().to_list()
    return create_response(
        success=True, data={"roles": [await role.to_public_dict() for role in roles]}
    )
