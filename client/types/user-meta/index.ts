import { User } from "..";

export interface UserMeta {
  uuid: string;
  data: string;
  user: User;
  status: boolean;
  created_at: string;
  updated_at: string;
  deleted_at: string;
}
