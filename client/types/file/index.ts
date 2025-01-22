export interface File {
  uuid: string;
  file_name: string;
  key: string;
  file_type: string;
  url: string;
  status: boolean;
  created_at: string;
  updated_at: string;
  deleted_at: string;
}

export interface DownloadLink {
  download_link: string;
}

export enum ValidMimeType {
  // Images
  PNG = "image/png",
  JPEG = "image/jpeg",
  JPG = "image/jpg",
  GIF = "image/gif",
  SVG = "image/svg+xml",
  WEBP = "image/webp",
  BMP = "image/bmp",
  TIFF = "image/tiff",

  // Videos
  MP4 = "video/mp4",
  WEBM_VIDEO = "video/webm",
  OGG_VIDEO = "video/ogg",
  QUICKTIME = "video/quicktime",
  AVI = "video/x-msvideo",
  WMV = "video/x-ms-wmv",

  // Audio
  MPEG_AUDIO = "audio/mpeg",
  OGG_AUDIO = "audio/ogg",
  WAV = "audio/wav",
  WEBM_AUDIO = "audio/webm",
  WMA = "audio/x-ms-wma",
  AAC = "audio/aac",

  // Documents
  PDF = "application/pdf",
  MS_WORD = "application/msword",
  MS_WORD_DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  MS_EXCEL = "application/vnd.ms-excel",
  MS_EXCEL_XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  MS_POWERPOINT = "application/vnd.ms-powerpoint",
  MS_POWERPOINT_PPTX = "application/vnd.openxmlformats-officedocument.presentationml.presentation",
  OPEN_DOC_TEXT = "application/vnd.oasis.opendocument.text",
  OPEN_DOC_SPREADSHEET = "application/vnd.oasis.opendocument.spreadsheet",
  TEXT_PLAIN = "text/plain",
  CSV = "text/csv",
  MARKDOWN = "text/markdown",
  JSON = "application/json",
  XML = "application/xml",
  ZIP = "application/zip",

  // Archives
  TAR = "application/x-tar",
  RAR = "application/x-rar-compressed",
  SEVEN_ZIP = "application/x-7z-compressed",

  // Other
  HTML = "text/html",
  JAVASCRIPT = "application/javascript",
  OCTET_STREAM = "application/octet-stream",
}

export function getAllValidMimeTypes(): ValidMimeType[] {
  return Object.values(ValidMimeType);
}

export function getEnumFromMimeType(
  validMimeTypes: ValidMimeType[] = [],
  mimeType: string,
): ValidMimeType | undefined {
  return Object.values(validMimeTypes).find((value) => value === mimeType);
}
