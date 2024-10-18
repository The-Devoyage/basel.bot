from datetime import datetime, timedelta
import os
import logging
from fastapi import APIRouter, HTTPException, WebSocket
import jwt
from pydantic import BaseModel

from database.role import RoleModel
from database.user import UserModel
from utils.environment import get_env_var
from utils.jwt import create_jwt

router = APIRouter()

logger = logging.getLogger(__name__)

# Environment variables
auth_secret = get_env_var("AUTH_SECRET")
access_secret = get_env_var("ACCESS_SECRET")
jwt_algorithm = get_env_var("JWT_ALGORITHM")
client_url = get_env_var("CLIENT_URL")

# Database
role_model = RoleModel("basel.db")
user_model = UserModel("basel.db")

active_auth_connections = {}


@router.post("/logout")
def logout():
    pass


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
            auth_data = AuthStart.parse_raw(data)

            logger.debug(f"Auth data: {auth_data}")

            if not auth_data.email:
                raise ValueError("Email is required")

            user = user_model.get_user_by_email(cursor, auth_data.email)
            if not user:
                user_id = user_model.create_user(
                    cursor=cursor,
                    email=auth_data.email,
                )
                user = user_model.get_user_by_id(cursor, user_id)
                if not user:
                    raise ValueError("Failed to create user")

            expire_time = datetime.utcnow() + timedelta(minutes=3)

            token = create_jwt(
                {"uuid": user.uuid, "auth_id": user.auth_id, "exp": expire_time}, secret
            )
            magic_link = f"{client_url}/auth/{token}"

            logger.debug(f"Magic link: {magic_link}")

            connection.commit()

            active_auth_connections[user.auth_id] = websocket

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
    # Decode the token
    if not auth_finish.token or auth_finish.token is None:
        return HTTPException(status_code=400, detail="Token is required")
    try:
        payload = jwt.decode(auth_finish.token, auth_secret, algorithms=[jwt_algorithm])
        connection = user_model._get_connection()
        cursor = connection.cursor()
        user = user_model.get_user_by_auth_id(cursor, payload["auth_id"])
        if not user:
            raise Exception("User not found")

        user_id = user_model.update_user(cursor, user.id, status=True)
        if not user_id:
            raise Exception("Failed to activate user.")

        connection.commit()

        expire_time = datetime.utcnow() + timedelta(hours=24)

        token = create_jwt(
            {"uuid": user.uuid, "auth_id": user.auth_id, "exp": expire_time},
            access_secret,
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

        return {"success": True}

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
