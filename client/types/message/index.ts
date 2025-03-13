import { Endpoint } from "@/api";
import { File, User } from "@/types";

export interface Button {
  label: string;
  action:
    | { type: "call"; endpoint: Endpoint.SubscribeStart }
    | { type: "redirect"; endpoint: string };
}

export enum ChatMode {
  CHAT = "chat",
  INTERVIEW = "interview",
}

export interface SocketMessage {
  text: string;
  timestamp: Date;
  sender: "user" | "bot";
  buttons?: Button[];
  files?: File[];
  context?: string;
  message_type: "message" | "end";
  chat_mode: ChatMode;
}

export interface Message {
  user: User;
  sender: "user" | "bot";
  text: string;
  created_at: string;
  chat_mode: ChatMode;
}
