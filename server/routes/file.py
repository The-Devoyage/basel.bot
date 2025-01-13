import logging
from fastapi import APIRouter, Depends, HTTPException
from utils.boto import vultr_s3_client
from utils.environment import get_env_var
from utils.responses import create_response
from utils.jwt import require_auth, UserClaims


router = APIRouter()

logger = logging.getLogger(__name__)

VULTR_S3_BUCKET = get_env_var("VULTR_S3_BUCKET")

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@router.get("/file-upload-link")
async def get_file_upload_link(
    file_name: str, file_size: int, _: UserClaims = Depends(require_auth)
):
    try:
        # Validate file size
        if file_size > MAX_FILE_SIZE:
            return HTTPException(
                status_code=400,
                detail=f"File size exceeds the limit of {MAX_FILE_SIZE // (1024 * 1024)} MB.",
            )

        response = vultr_s3_client.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": VULTR_S3_BUCKET,
                "Key": file_name,
                "ContentLength": file_size,
            },
            ExpiresIn=300,
        )

        return create_response(
            success=True,
            data={"upload_link": response},
        )
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")
