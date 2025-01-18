from typing import List
from database.base import BaseMongoModel
from utils.environment import get_env_var
from utils.boto import vultr_s3_client

VULTR_S3_BUCKET = get_env_var("VULTR_S3_BUCKET")


class File(BaseMongoModel):
    file_name: str
    key: str
    file_type: str
    tags: List[str] = []
    status: bool = True

    def get_virtual_fields(self) -> dict:
        profile_image_url = vultr_s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": VULTR_S3_BUCKET, "Key": self.key},
            ExpiresIn=300,
        )

        return {"url": profile_image_url}
