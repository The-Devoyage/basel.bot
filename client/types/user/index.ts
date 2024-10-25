export interface User {
  uuid: string;
  email: string;
  first_name: string;
  last_name: string;
  phone: string;
  role_id: number;
  status: boolean;
  file: number;
  created_by: number;
  updated_by: number;
  deleted_by: number;
  created_at: string;
  updated_at: string;
  deleted_at: string;
}
