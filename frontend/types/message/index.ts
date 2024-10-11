import { Posting } from "../product";

export interface Message {
  text: string;
  timestamp: Date;
  sender: "user" | "bot";
  products?: Product[];
}
