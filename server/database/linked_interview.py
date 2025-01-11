from beanie import Link
from database.base import BaseMongoModel
from database.interview import Interview
from database.shareable_link import ShareableLink


class LinkedInterview(BaseMongoModel):
    interview: Link[Interview]
    shareable_link: Link[ShareableLink]
