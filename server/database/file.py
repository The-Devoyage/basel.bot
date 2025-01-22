from typing import List
from database.base import BaseMongoModel
from utils.environment import get_env_var
from utils.boto import vultr_s3_client

VULTR_S3_BUCKET = get_env_var("VULTR_S3_BUCKET")

from enum import Enum


class MimeType(str, Enum):
    # Images
    IMAGE_PNG = "image/png"
    IMAGE_JPEG = "image/jpeg"
    IMAGE_JPG = "image/jpg"
    IMAGE_GIF = "image/gif"
    IMAGE_SVG = "image/svg+xml"
    IMAGE_WEBP = "image/webp"
    IMAGE_BMP = "image/bmp"
    IMAGE_TIFF = "image/tiff"
    # Videos
    VIDEO_MP4 = "video/mp4"
    VIDEO_WEBM = "video/webm"
    VIDEO_OGG = "video/ogg"
    VIDEO_QUICKTIME = "video/quicktime"
    VIDEO_AVI = "video/x-msvideo"
    VIDEO_WMV = "video/x-ms-wmv"
    # Audio
    AUDIO_MPEG = "audio/mpeg"
    AUDIO_OGG = "audio/ogg"
    AUDIO_WAV = "audio/wav"
    AUDIO_WEBM = "audio/webm"
    AUDIO_WMA = "audio/x-ms-wma"
    AUDIO_AAC = "audio/aac"
    # Documents
    APPLICATION_PDF = "application/pdf"
    APPLICATION_WORD_DOC = "application/msword"
    APPLICATION_WORD_DOCX = (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    APPLICATION_EXCEL_XLS = "application/vnd.ms-excel"
    APPLICATION_EXCEL_XLSX = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    APPLICATION_PPT = "application/vnd.ms-powerpoint"
    APPLICATION_PPTX = (
        "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )
    APPLICATION_ODT = "application/vnd.oasis.opendocument.text"
    APPLICATION_ODS = "application/vnd.oasis.opendocument.spreadsheet"
    TEXT_PLAIN = "text/plain"
    TEXT_CSV = "text/csv"
    TEXT_MARKDOWN = "text/markdown"
    APPLICATION_JSON = "application/json"
    APPLICATION_XML = "application/xml"
    APPLICATION_ZIP = "application/zip"
    # Archives
    APPLICATION_TAR = "application/x-tar"
    APPLICATION_RAR = "application/x-rar-compressed"
    APPLICATION_7Z = "application/x-7z-compressed"
    # Other
    TEXT_HTML = "text/html"
    APPLICATION_JS = "application/javascript"
    APPLICATION_OCTET_STREAM = "application/octet-stream"


class File(BaseMongoModel):
    file_name: str
    key: str
    file_type: MimeType
    tags: List[str] = []
    status: bool = True

    def get_virtual_fields(self) -> dict:
        profile_image_url = vultr_s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": VULTR_S3_BUCKET, "Key": self.key},
            ExpiresIn=300,
        )

        return {"url": profile_image_url}
