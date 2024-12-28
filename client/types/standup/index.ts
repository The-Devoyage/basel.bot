import { User } from "../user";

export interface Standup {
  uuid: string;
  user: User;
  yesterday: string;
  today: string;
  blockers: string;
  status: boolean;
  created_at: string;
  updated_at: string;
  deleted_at: string;
}
