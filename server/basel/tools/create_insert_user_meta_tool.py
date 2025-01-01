from chromadb.api.models.Collection import logging
from llama_index.core.tools.function_tool import FunctionTool
from pydantic import BaseModel, Field
from database.user import User
from database.user_meta import UserMeta
from database.notification import Notification, NotificationType
from utils.notification import get_user_notification_socket

logger = logging.getLogger(__name__)


class InsertUserMetaToolParams(BaseModel):
    fact: str = Field(
        description="""
                      A `professional` career related fact to be saved about the user. This can include:
                      - Career Skills
                      - Education Facts
                      - Hobbies and Personal Interests
                      - Career History
                      - Projects and/or Related Interests
                      """
    )


async def insert_user_meta(user: User, fact: str):
    user_meta = None
    try:
        user_meta = UserMeta(
            user=user,  # type:ignore
            data=fact,
            created_by=user,  # type:ignore
        )
        await user_meta.save()

        return user_meta
    except Exception as e:
        logger.error(f"Error saving user_meta: {e}")
        return "Something went wrong."
    finally:
        try:
            # Create and send notification
            notification = Notification(
                user=user,  # type:ignore
                created_by=user,  # type:ignore
                type=NotificationType.META_ADDED,
                text=user_meta.data
                if user_meta
                else "Basel has added a new memory to your index.",
            )
            await notification.save()

            # Send notification via WebSocket
            websocket = get_user_notification_socket(user)
            if not websocket or websocket is None:
                logger.warn("WEBSOCKET NOT FOUND")
            else:
                await websocket.send_json(await notification.to_public_dict(json=True))
        except Exception as e:
            # Log errors in the notification process
            logger.error(f"Error in notification process: {e}")


def create_insert_user_meta_tool(user: User):
    insert_user_meta_tool = FunctionTool.from_defaults(
        name="insert_user_meta_tool",
        description="""
            Useful to save identified career facts about the candidate throughout the conversation as needed.
            Anytime a user highlights skills, career facts, hobbies, or personal interests, use this tool to log it to your database.
            """,
        async_fn=lambda fact: insert_user_meta(user, fact),
        fn_schema=InsertUserMetaToolParams,
    )
    return insert_user_meta_tool
