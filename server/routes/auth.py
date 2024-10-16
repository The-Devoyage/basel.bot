import os
import logging
import sqlite3
from fastapi import APIRouter, HTTPException, WebSocket
import jwt
from pydantic import BaseModel, ValidationError

from database.role import RoleModel
from database.user import UserModel
from utils.jwt import create_jwt

router = APIRouter()

logger = logging.getLogger(__name__)

# Database
role_model = RoleModel("basel.db")
user_model = UserModel("basel.db")

active_register_connections = {}


@router.post("/login")
def login():
    pass


@router.post("/logout")
def logout():
    pass


class RegisterStart(BaseModel):
    email: str


@router.websocket("/register-start")
async def register_start(websocket: WebSocket):
    await websocket.accept()

    # Get the connection
    connection = user_model._get_connection()
    cursor = connection.cursor()

    secret = os.getenv("REGISTER_SECRET")
    if not secret:
        raise ValueError("REGISTER_SECRET environment variable not set")

    while True:
        try:
            data = await websocket.receive_text()
            register_data = RegisterStart.parse_raw(data)

            logger.debug(f"Register data: {register_data}")

            if not register_data.email:
                raise ValueError("Email is required")

            user_id = user_model.create_user(
                cursor=cursor,
                email=register_data.email,
            )

            user = user_model.get_user_by_id(cursor, user_id)
            if not user:
                raise ValueError("Failed to create user")

            create_jwt({"uuid": user["uuid"], "auth_id": user["auth_id"]}, secret)

            connection.commit()

            logger.debug(f"User created: {user}")
            logger.debug(f"JWT: {jwt}")

            active_register_connections[user["auth_id"]] = websocket

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


@router.post("/register-finish")
def register_finish(token: str):
    # Decode the token
    register_secret = os.getenv("REGISTER_SECRET")
    if not register_secret:
        raise Exception("REGISTER_SECRET not set")
    auth_secret = os.getenv("AUTH_SECRET")
    if not auth_secret:
        raise Exception("AUTH_SECRET not set")
    try:
        payload = jwt.decode(token, register_secret)
        connection = user_model._get_connection()
        cursor = connection.cursor()
        user = user_model.get_user_by_auth_id(cursor, payload["auth_id"])
        if not user:
            raise Exception("User not found")

        user_id = user_model.update_user(cursor, user["id"], status=True)
        if not user_id:
            raise Exception("Failed to activate user.")

        connection.commit()

        auth_token = create_jwt(
            {"uuid": user["uuid"], "auth_id": user["auth_id"]}, auth_secret
        )

        active_register_connections[payload["auth_id"]].send_json(
            {
                "success": True,
                "auth_token": auth_token,
            }
        )

        # Send the JWT to the user waiting on the websocket

        return {"success": True}

    except jwt.ExpiredSignatureError:
        return HTTPException(status_code=401, detail="Expired token")
    except jwt.InvalidTokenError:
        return HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error decoding token: {e}")
