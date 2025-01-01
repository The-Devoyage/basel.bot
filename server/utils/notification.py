from chromadb.api.models.Collection import Optional, logging
from fastapi import WebSocket
from database.user import User
from routes.notification import active_channels

logger = logging.getLogger(__name__)


def get_user_notification_socket(user: User) -> Optional[WebSocket]:
    logger.debug("GETTING USER NOTIFICATION SOCKET")
    logger.debug(active_channels)
    websocket = active_channels[str(user.uuid)]
    return websocket
