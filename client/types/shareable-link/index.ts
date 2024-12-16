import { User } from "../user";

export interface ShareableLink {
  uuid: string;
  tag: string;
  link: string;
  status: boolean;
  user: User;
  created_at: string;
  updated_at: string;
  deleted_at: string;
}
