import { Endpoint } from "@/api";

export interface Button {
  label: string;
  action: { type: "call"; endpoint: Endpoint.SubscribeStart };
}

export interface Message {
  text: string;
  timestamp: Date;
  sender: "user" | "bot";
  buttons?: Button[];
}
