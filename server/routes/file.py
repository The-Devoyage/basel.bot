import logging
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from beanie import SortDirection
from beanie.operators import In
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from utils.boto import vultr_s3_client
from utils.environment import get_env_var
from utils.responses import create_response
from utils.jwt import require_auth, UserClaims
from database.file import File, MimeType


router = APIRouter()

logger = logging.getLogger(__name__)

VULTR_S3_BUCKET = get_env_var("VULTR_S3_BUCKET")

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@router.get("/download-link")
async def get_download_link(uuid: str, user_claims: UserClaims = Depends(require_auth)):
    try:
        file = await File.find_one(
            File.uuid == UUID(uuid),
            File.created_by.id == user_claims.user.id,  # type:ignore
        )

        if not file:
            return HTTPException(
                status_code=400,
                detail=f"File not found.",
            )

        response = vultr_s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": VULTR_S3_BUCKET, "Key": file.key},
            ExpiresIn=300,
        )

        return create_response(
            success=True,
            data={"download_link": response},
        )

    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")


@router.get("/upload-link")
async def get_file_upload_link(
    file_name: str,
    file_size: int,
    mimetype: MimeType,
    user_claims: UserClaims = Depends(require_auth),
):
    try:
        # Validate file size
        if file_size > MAX_FILE_SIZE:
            logger.error("EXCEEDS MAX ALLOWED FILE SIZE")
            return HTTPException(
                status_code=400,
                detail=f"File size exceeds the limit of {MAX_FILE_SIZE // (1024 * 1024)} MB.",
            )

        if mimetype not in MimeType.__members__.values():
            logger.error("INVALID FILE TYPE")
            return HTTPException(
                status_code=400,
                detail="The submitted mimetype is unsupported.",
            )

        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        s3_key = f"{timestamp}_{file_name}"

        response = vultr_s3_client.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": VULTR_S3_BUCKET,
                "Key": s3_key,
                "ContentLength": file_size,
            },
            ExpiresIn=300,
        )

        file = await File(
            file_name=file_name,
            key=s3_key,
            file_type=mimetype,
            created_by=user_claims.user,  # type:ignore
            status=False,
        ).create()

        return create_response(
            success=True,
            data={"upload_link": response, "file_uuid": file.uuid},
        )
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")


class CreateFileParams(BaseModel):
    uuid: str


@router.patch("/activate")
async def activate_file(
    params: CreateFileParams,
    user_claims: UserClaims = Depends(require_auth),
):
    try:
        file = await File.find_one(
            File.uuid == UUID(params.uuid),
            File.created_by.id == user_claims.user.id,  # type:ignore
        )

        if not file:
            return HTTPException(status_code=500, detail="Failed to find file.")

        file.status = True
        file.updated_by = user_claims.user  # type:ignore

        await file.save()

        return create_response(success=True, data=await file.to_public_dict())

    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")


@router.get("/list")
async def get_files(
    file_types: Optional[List[MimeType]] = Query(None),
    offset: int = 0,
    limit: int = 10,
    user_claims: UserClaims = Depends(require_auth),
):
    logger.debug(f"LIMIT {type(limit)} OFFSET {type(offset)}, FILETYPES: {file_types}")
    try:
        query = File.find(
            File.created_by.id == user_claims.user.id,  # type:ignore
            File.status == True,
        )

        if file_types:
            logger.debug(f"FILETYPES: {file_types}")
            query.find(In(File.file_type, [ft.value for ft in file_types]))

        files = (
            await query.find()
            .limit(limit)
            .skip(offset)
            .sort(
                [(File.created_at, SortDirection.DESCENDING)]  # type:ignore
            )
            .to_list()
        )

        total = await query.find().count()

        return create_response(
            success=True,
            data=[await file.to_public_dict() for file in files],
            total=total,
        )

    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")
