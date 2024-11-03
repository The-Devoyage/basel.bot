from datetime import datetime, timedelta
import os
import logging
from fastapi import APIRouter, Depends, HTTPException, WebSocket
import jwt
import uuid
from pydantic import BaseModel
from classes.user_claims import UserClaims

from database.role import RoleModel
from database.token_session import TokenSessionModel
from database.user import UserModel
from utils.environment import get_env_var
from utils.jwt import create_jwt, require_auth
from utils.mailer import send_email
from utils.responses import create_response

router = APIRouter()

logger = logging.getLogger(__name__)

# Environment variables
AUTH_SECRET = get_env_var("AUTH_SECRET")
ACCESS_SECRET = get_env_var("ACCESS_SECRET")
JWT_ALGO = get_env_var("JWT_ALGORITHM")
CLIENT_URL = get_env_var("CLIENT_URL")

# Database
role_model = RoleModel("basel.db")
user_model = UserModel("basel.db")
token_session_model = TokenSessionModel("basel.db")

active_auth_connections = {}


@router.get("/verify")
def verify(user_claims: UserClaims = Depends(require_auth)):
    connection = token_session_model._get_connection()
    cursor = connection.cursor()
    try:
        token_session = token_session_model.get_token_session_by_uuid(
            cursor, user_claims.token_session_uuid
        )
        if not token_session:
            raise Exception("Token session not found")

        return create_response(success=True, data=None)
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=401, detail="Invalid token")


@router.get("/me")
def me(user_claims: UserClaims = Depends(require_auth)):
    connection = user_model._get_connection()
    cursor = connection.cursor()
    try:
        user = user_model.get_user_by_uuid(cursor, user_claims.user_uuid)
        if not user:
            raise Exception("User not found")
        return create_response(success=True, data=user.to_public_dict())
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=401, detail="Invalid token")


@router.post("/logout")
def logout(user_claims: UserClaims = Depends(require_auth)):
    try:
        connection = user_model._get_connection()
        cursor = connection.cursor()

        logger.debug(f"User claims: {user_claims}")

        invalidated = token_session_model.invalidate_token_session(
            cursor, user_claims.token_session_uuid
        )

        if not invalidated:
            raise Exception("Failed to invalidate token session.")

        connection.commit()
        return create_response(success=True, data=None)
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Failed to logout user")


class AuthStart(BaseModel):
    email: str


@router.websocket("/auth-start")
async def auth_start(websocket: WebSocket):
    await websocket.accept()

    # Get the connection
    connection = user_model._get_connection()
    cursor = connection.cursor()

    secret = os.getenv("AUTH_SECRET")
    if not secret:
        raise ValueError("AUTH_SECRET environment variable not set")

    while True:
        try:
            data = await websocket.receive_text()
            auth_data = AuthStart.model_validate_json(data)

            logger.debug(f"Auth data: {auth_data}")

            if not auth_data.email:
                raise ValueError("Email is required")

            current_user = user_model.get_user_by_email(cursor, auth_data.email)
            if not current_user:
                logger.debug("User not found, creating new user")
                user_id = user_model.create_user(
                    cursor=cursor,
                    email=auth_data.email,
                )
                current_user = user_model.get_user_by_id(cursor, user_id)
                if not current_user:
                    raise ValueError("Failed to create user")
            else:
                logger.debug("User found, updating user")
                user_id = user_model.update_user(
                    cursor,
                    current_user.id,
                    auth_id=str(uuid.uuid4()),
                    current_user=current_user,
                )
                current_user = user_model.get_user_by_id(cursor, user_id)
                if not current_user:
                    raise ValueError("Failed to update user")

            expire_time = datetime.utcnow() + timedelta(minutes=3)

            token = create_jwt(
                {
                    "uuid": current_user.uuid,
                    "auth_id": current_user.auth_id,
                    "exp": expire_time,
                },
                secret,
            )
            magic_link = f"{CLIENT_URL}/auth/{token}"

            logger.debug(f"Magic link: {magic_link}")

            connection.commit()

            active_auth_connections[current_user.auth_id] = websocket

            send_email(
                current_user.email,
                "Magic Link - Click and Authenticate",
                "d-647b376beee74b30aff1b669af7a7392",
                {"magic_link": magic_link},
            )

            await websocket.send_json(
                {
                    "success": True,
                }
            )

        except Exception as e:
            logger.error(e)
            await websocket.send_json(
                {"success": False, "message": "Something went wrong. Please try again."}
            )


class AuthFinish(BaseModel):
    token: str


@router.post("/auth-finish")
async def auth_finish(auth_finish: AuthFinish):
    logger.debug(f"Auth Finish: {auth_finish}")
    # Decode the token
    if not auth_finish.token or auth_finish.token is None:
        return HTTPException(status_code=400, detail="Token is required")

    connection = user_model._get_connection()
    cursor = connection.cursor()

    try:
        payload = jwt.decode(auth_finish.token, AUTH_SECRET, algorithms=[JWT_ALGO])
        logger.debug(f"AuthID: {payload['auth_id']}")
        current_user = user_model.get_user_by_auth_id(cursor, payload["auth_id"])
        if not current_user:
            raise Exception("User not found")

        user_id = user_model.update_user(
            cursor, current_user.id, status=True, current_user=current_user
        )
        if not user_id:
            raise Exception("Failed to activate user.")

        token_session_id = token_session_model.create_token_session(
            cursor, current_user.id
        )
        if not token_session_id:
            raise Exception("Failed to create token session")

        token_session = token_session_model.get_token_session_by_id(
            cursor, token_session_id
        )

        if not token_session:
            raise Exception("Failed to get token session")

        connection.commit()

        expire_time = datetime.utcnow() + timedelta(hours=24)

        token = create_jwt(
            {
                "user_uuid": current_user.uuid,
                "auth_id": current_user.auth_id,
                "exp": expire_time,
                "token_session_uuid": token_session.uuid,
            },
            ACCESS_SECRET,
        )

        auth_connection = active_auth_connections.get(payload["auth_id"])

        if not auth_connection:
            return HTTPException(
                status_code=400, detail="No active connection found for user"
            )

        await auth_connection.send_json(
            {
                "success": True,
                "token": token,
                "message": "User authenticated successfully",
            }
        )

        return create_response(success=True, data=None)

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
        connection.rollback()
        return HTTPException(status_code=500, detail=f"Error decoding token: {e}")
