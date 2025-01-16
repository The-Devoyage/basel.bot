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
