from functools import partial
from chromadb.api.models.Collection import logging
from llama_index.core.tools.function_tool import FunctionTool
from pydantic import BaseModel, Field
from database.subscription import SubscriptionFeature
from database.user import User
from database.user_meta import UserMeta
from database.notification import Notification, NotificationType
from utils.notification import get_user_notification_socket
from utils.subscription import SubscriptionStatus, check_subscription_permission

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


async def insert_user_meta(
    current_user: User, fact: str, subscription_status: SubscriptionStatus
):
    user_meta = None

    allow_insert = check_subscription_permission(
        subscription_status, SubscriptionFeature.CREATE_INTERVIEW
    )

    if not allow_insert:
        raise Exception(
            "The user's free trial has expired and they are not a member. This feature is disabled. Encourage them to subscribe."
        )

    try:
        user_meta = UserMeta(
            user=current_user,  # type:ignore
            data=fact,
            created_by=current_user,  # type:ignore
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
                user=current_user,  # type:ignore
                created_by=current_user,  # type:ignore
                type=NotificationType.META_ADDED,
                text=user_meta.data
                if user_meta
                else "Basel has added a new memory to your index.",
            )
            await notification.save()

            # Send notification via WebSocket
            websocket = get_user_notification_socket(current_user)
            if not websocket or websocket is None:
                logger.warn("WEBSOCKET NOT FOUND")
            else:
                await websocket.send_json(await notification.to_public_dict(json=True))
                return True
        except Exception as e:
            # Log errors in the notification process
            logger.error(f"Error in notification process: {e}")
            return False


def init_insert_user_meta_tool(
    current_user: User, subscription_status: SubscriptionStatus
):
    insert_user_meta_tool = FunctionTool.from_defaults(
        name="insert_user_meta_tool",
        description="""
           Useful to save memories about the user including details about the users career, goals, hobbies, and job search.
        """,
        async_fn=partial(
            insert_user_meta,
            current_user=current_user,
            subscription_status=subscription_status,
        ),
        fn_schema=InsertUserMetaToolParams,
    )
    return insert_user_meta_tool
