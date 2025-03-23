import logging
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import (
    init_beanie,
)
from database.interview_transcript import InterviewTranscript
from database.organization import Organization
from database.organization_user import OrganizationUser
from database.standup import Standup
from database.user import User
from database.user_meta import UserMeta
from database.token_session import TokenSession
from database.subscription import Subscription
from database.shareable_link import ShareableLink
from database.role import Role, RoleIdentifier
from database.message import Message
from database.interview_question import InterviewQuestion
from database.interview import Interview
from database.notification import Notification
from database.file import File
from database.interview_assessment import InterviewAssessment
from utils.environment import get_env_var

logger = logging.getLogger(__name__)

# Constants
DB_URI = get_env_var("DB_URI")
DB_DATABASE = get_env_var("DB_DATABASE")


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
    client = AsyncIOMotorClient(
        f"{DB_URI}",
        uuidRepresentation="standard",
    )
    await init_beanie(
        database=client.basel,
        document_models=[
            User,
            UserMeta,
            Interview,
            InterviewQuestion,
            TokenSession,
            Subscription,
            ShareableLink,
            Role,
            Message,
            Standup,
            Notification,
            File,
            Organization,
            OrganizationUser,
            InterviewAssessment,
            InterviewTranscript,
        ],
        allow_index_dropping=True,
    )
    await sync_roles()
    return client
