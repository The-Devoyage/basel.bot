import { User } from "..";

export enum NotificationType {
  GENERAL = "general",
  META_ADDED = "meta_added",
}

export interface Notification {
  user: User;
  uuid: string;
  text: string;
  type: NotificationType;
  read: boolean;
  created_at: string;
}
