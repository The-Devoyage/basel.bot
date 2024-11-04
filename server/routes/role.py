import logging
from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends
from classes.user_claims import UserClaims
from database.role import RoleModel

from utils.jwt import require_auth
from utils.responses import create_response

router = APIRouter()

logger = logging.getLogger(__name__)

# Database
role_model = RoleModel("basel.db")


@router.get("/role")
async def role(id: int, _: UserClaims = Depends(require_auth)):
    conn = role_model._get_connection()
    cursor = conn.cursor()
    role = role_model.get_role_by_id(cursor, id)

    if not role or role is None:
        raise HTTPException(status_code=404, detail="Role not found")

    return create_response(success=True, data={"role": role})


@router.get("/roles")
async def roles(_: UserClaims = Depends(require_auth)):
    conn = role_model._get_connection()
    cursor = conn.cursor()
    roles = role_model.get_roles(cursor)
    return create_response(success=True, data={"roles": roles})
