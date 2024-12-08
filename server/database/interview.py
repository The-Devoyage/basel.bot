from database.base import BaseMongoModel


class Interview(BaseMongoModel):
    name: str
    description: str
    status: bool = True
