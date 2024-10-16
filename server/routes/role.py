import logging
from fastapi import APIRouter, HTTPException
from database.role import RoleModel

router = APIRouter()

logger = logging.getLogger(__name__)

# Database
role_model = RoleModel("basel.db")


@router.get("/role")
async def role(id: int):
    conn = role_model._get_connection()
    cursor = conn.cursor()
    role = role_model.get_role_by_id(cursor, id)

    if not role or role is None:
        raise HTTPException(status_code=404, detail="Role not found")

    return {"role": role}  # Return the role data if found


@router.get("/roles")
async def roles():
    conn = role_model._get_connection()
    cursor = conn.cursor()
    roles = role_model.get_roles(cursor)
    return {"roles": roles}
