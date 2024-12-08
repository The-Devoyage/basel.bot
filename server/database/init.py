import logging
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import (
    init_beanie,
)
from database.user import User
from database.user_meta import UserMeta
from database.token_session import TokenSession
from database.subscription import Subscription
from database.shareable_link import ShareableLink
from database.role import Role, RoleIdentifier
from database.message import Message
from database.interview_question import InterviewQuestion
from database.interview_question_response import InterviewQuestionResponse
from database.interview import Interview

logger = logging.getLogger(__name__)


async def sync_roles():
    admin_role = Role(identifier=RoleIdentifier.ADMIN, name="Admin")
    user_role = Role(identifier=RoleIdentifier.USER, name="User")
    roles = [admin_role, user_role]
    for role in roles:
        existing = await Role.find_one(Role.identifier == role.identifier)
        if not existing:
            await role.create()


async def init_db():
    logger.debug("INIT DB")
    client = AsyncIOMotorClient("mongodb://api:basel@localhost:27017/basel")
    await init_beanie(
        database=client.basel,
        document_models=[
            User,
            UserMeta,
            Interview,
            InterviewQuestionResponse,
            InterviewQuestion,
            TokenSession,
            Subscription,
            ShareableLink,
            Role,
            Message,
        ],
        allow_index_dropping=True,
    )
    await sync_roles()
    return client
