import logging
from typing import Optional
from beanie import SortDirection
from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
    WebSocketException,
    status,
)
from classes.user_claims import UserClaims
from database.notification import Notification

from utils.jwt import handle_decode_token, require_auth, verify_token_session
from utils.responses import create_response

logger = logging.getLogger(__name__)

router = APIRouter()

active_channels = {}


@router.websocket("/notification")
async def socket_notification(
    websocket: WebSocket,
    token: str = Cookie(None),
):
    current_user = None
    await websocket.accept()

    # Require Auth
    try:
        if not token:
            raise Exception("Authentication Required")
        user_claims = await handle_decode_token(token)
        await verify_token_session(user_claims.token_session_uuid)
        current_user = user_claims.user
    except Exception as e:
        logger.error(e)
        return WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

    # Add user socket to activve channels
    try:
        active_channels[str(current_user.uuid)] = websocket
        while True:
            # TODO: mark the notification read in real time
            # For now, play ping pong.
            data = await websocket.receive_text()
            return data

    except WebSocketDisconnect as e:
        logger.debug("REMOVING CONNECTION")
        if current_user and current_user.uuid in active_channels:
            del active_channels[current_user.uuid]
            logger.info(f"Removed connection for uuid: {current_user.uuid}")

    except Exception as e:
        logger.error(e)


@router.get("/notifications")
async def get_notifications(
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    read: Optional[bool] = None,
    user_claims: UserClaims = Depends(require_auth),
):
    try:
        notifications = Notification.find_many(
            Notification.user.id == user_claims.user.id,  # type:ignore
            fetch_links=True,
        )

        if read is not None:
            notifications.find(Notification.read == read)

        notifications = (
            await notifications.limit(limit)
            .skip(offset)
            .sort(
                [(Notification.created_at, SortDirection.DESCENDING)]  # type:ignore
            )
            .to_list()
        )

        return create_response(
            success=True, data=[await n.to_public_dict() for n in notifications]
        )
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")
