from typing import Optional
from beanie import WriteRules
import jwt
import uuid
import logging
from uuid import UUID
from beanie.operators import Set
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, WebSocket
from pydantic import BaseModel
from classes.user_claims import UserClaims
from database.token_session import TokenSession
from database.user import User
from database.role import Role, RoleIdentifier

from utils.environment import get_env_var
from utils.jwt import create_jwt, require_auth
from mailer import send_email
from utils.responses import create_response

router = APIRouter()

logger = logging.getLogger(__name__)

# Environment variables
AUTH_SECRET = get_env_var("AUTH_SECRET")
ACCESS_SECRET = get_env_var("ACCESS_SECRET")
JWT_ALGO = get_env_var("JWT_ALGORITHM")
CLIENT_URL = get_env_var("CLIENT_URL")

active_auth_connections = {}


@router.get("/verify")
async def verify(user_claims: UserClaims = Depends(require_auth)):
    try:
        token_session = await TokenSession.find_one(
            TokenSession.uuid == UUID(user_claims.token_session_uuid)
        )

        if not token_session:
            raise Exception("Token session not found")

        return create_response(success=True, data=None)
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=401, detail="Invalid token")


@router.get("/me")
async def me(user_claims: UserClaims = Depends(require_auth)):
    logger.debug(f"FETCHING ME: {user_claims}")
    try:
        user = await User.find_one(
            User.uuid == UUID(user_claims.user_uuid), fetch_links=True
        )
        if not user:
            raise Exception("User not found")
        return create_response(success=True, data=await user.to_public_dict())
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=401, detail="Invalid token")


@router.post("/logout")
async def logout(user_claims: UserClaims = Depends(require_auth)):
    try:
        token_session = await TokenSession.find_one(
            TokenSession.uuid == UUID(user_claims.token_session_uuid)
        )

        if not token_session:
            raise Exception("Failed to find token session")

        token_session.status = False
        token_session.updated_by = user_claims.user  # type:ignore
        await token_session.save()

        return create_response(success=True, data=None)
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Failed to logout user")


class AuthStart(BaseModel):
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


@router.websocket("/auth-start")
async def auth_start(websocket: WebSocket):
    logger.debug("AUTH START")

    # Start Connection
    await websocket.accept()

    # Global Scope
    current_user = None

    try:
        while True:
            data = await websocket.receive_text()
            auth_data = AuthStart.model_validate_json(data)

            logger.debug(f"Auth data: {auth_data}")

            if not auth_data.email:
                raise ValueError("Email is required")

            # Find or create current user
            current_user = await User.find_one(User.email == auth_data.email)
            if not current_user:
                logger.debug("CREATING NEW USER")
                role = await Role.find_one(Role.identifier == RoleIdentifier.USER)
                if not role:
                    raise ValueError("Role not found")
                logger.debug(f"FOUND ROLE: {role}")
                current_user = await User(
                    email=auth_data.email, role=role  # type: ignore
                ).insert(link_rule=WriteRules.DO_NOTHING)
                logger.debug(f"USER CREATED: {current_user}")
                if not current_user:
                    raise ValueError("Failed to create user")

                # Send user created email
                full_name = current_user.full_name()
                send_email(
                    ["nickmclean@thedevoyage.com"],
                    "d-d526a9167b6240bbbc8a99a2fb1ab387",
                    {
                        "name": full_name if full_name else "the user",
                        "email": current_user.email,
                    },
                )

            else:
                logger.debug(f"UPDATING USER: {current_user}")
                current_user = await current_user.update(Set({"auth_id": uuid.uuid4()}))
                if not current_user:
                    raise ValueError("Failed to update user")

            # Create Sign In Token
            logger.debug("CREATING TOKEN")
            expire_time = datetime.utcnow() + timedelta(minutes=10)
            token = create_jwt(
                {
                    "uuid": str(current_user.uuid),
                    "auth_id": str(current_user.auth_id),
                    "exp": expire_time,
                },
                AUTH_SECRET,
            )
            magic_link = f"{CLIENT_URL}/auth/{token}"

            logger.info(
                f"""
                User: {current_user.email}
                Magic link: {magic_link}
                """
            )

            active_auth_connections[str(current_user.auth_id)] = websocket

            send_email(
                [current_user.email],
                "d-647b376beee74b30aff1b669af7a7392",
                {"magic_link": magic_link},
            )

            await websocket.send_json(
                {"success": True, "auth_id": str(current_user.auth_id)}
            )

    except Exception as e:
        logger.error(e)
        await websocket.send_json(
            {"success": False, "message": "Something went wrong. Please try again."}
        )

    finally:
        if current_user and current_user.auth_id in active_auth_connections:
            del active_auth_connections[current_user.auth_id]
            logger.info(f"Removed connection for auth_id: {current_user.auth_id}")


class AuthFinish(BaseModel):
    token: str


@router.post("/auth-finish")
async def auth_finish(auth_finish: AuthFinish):
    logger.debug("AUTH FINISH")
    logger.debug(f"PAYLOAD: {auth_finish}")
    # Decode the token
    if not auth_finish.token or auth_finish.token is None:
        return HTTPException(status_code=400, detail="Token is required")

    try:
        payload = jwt.decode(auth_finish.token, AUTH_SECRET, algorithms=[JWT_ALGO])
        logger.debug(f"AuthID: {payload['auth_id']}")
        current_user = await User.find_one(User.auth_id == UUID(payload["auth_id"]))
        if not current_user:
            raise Exception("User not found")

        current_user = await current_user.update(Set({"status": True}))

        if not current_user:
            raise Exception("Failed to activate user.")

        token_session = await TokenSession(
            user=current_user,  # type:ignore
            created_by=current_user,  # type:ignore
        ).insert()

        if not token_session:
            raise Exception("Failed to create token session")

        expire_time = datetime.utcnow() + timedelta(days=24)

        token = create_jwt(
            {
                "user_uuid": str(current_user.uuid),
                "auth_id": str(current_user.auth_id),
                "exp": expire_time,
                "token_session_uuid": str(token_session.uuid),
            },
            ACCESS_SECRET,
        )

        auth_connection = active_auth_connections.get(payload["auth_id"])

        if auth_connection:
            await auth_connection.send_json(
                {
                    "success": True,
                    "token": token,
                    "message": "User authenticated successfully",
                }
            )

        return create_response(success=True, data={"token": token})

    except jwt.ExpiredSignatureError as e:
        logger.error(e)
        return HTTPException(
            status_code=401, detail="The token has expired, please try again."
        )
    except jwt.InvalidTokenError as e:
        logger.error(e)
        return HTTPException(
            status_code=401, detail="Your token is invalid, please try again."
        )
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail=f"Error decoding token: {e}")
