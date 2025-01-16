import { File } from "@/types";

export interface User {
  uuid: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  profile_image?: File;
  phone: string;
  role_id: number;
  status: boolean;
  file: number;
  created_at: string;
  updated_at: string;
  deleted_at: string;
}
