import boto3
from utils.environment import get_env_var

VULTR_S3_HOSTNAME = get_env_var("VULTR_S3_HOSTNAME")
VULTR_S3_SECRET_KEY = get_env_var("VULTR_S3_SECRET_KEY")
VULTR_S3_ACCESS_KEY = get_env_var("VULTR_S3_ACCESS_KEY")

session = boto3.Session()
vultr_s3_client = session.client(
    "s3",
    **{
        "region_name": VULTR_S3_HOSTNAME.split(".")[0],
        "endpoint_url": "https://" + VULTR_S3_HOSTNAME,
        "aws_access_key_id": VULTR_S3_ACCESS_KEY,
        "aws_secret_access_key": VULTR_S3_SECRET_KEY,
    }
)
