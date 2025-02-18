from pydantic import BaseModel

from database.user import User
from utils.subscription import SubscriptionStatus


class UserClaims(BaseModel):
    exp: int
    user_uuid: str
    auth_id: str
    token_session_uuid: str
    user: User
    subscription_status: SubscriptionStatus


class ShareableLinkClaims(BaseModel):
    user_uuid: str
    shareable_link_uuid: str
