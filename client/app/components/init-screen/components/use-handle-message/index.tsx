"use client";

import { GlobalContext } from "@/app/provider";
import { Message } from "@/types";
import { useContext } from "react";

export type MessageType =
  | "interviews"
  | "bot"
  | "search"
  | "resume"
  | "translations"
  | "candidate"
  | "interview";

export const useHandleMessage = () => {
  const { client } = useContext(GlobalContext);

  const handleMessage = (type: MessageType, context?: string) => {
    let text = "";
    switch (type) {
      case "interviews":
        text =
          "I am interested in learning about Automated Interviews. How do these work?";
        break;
      case "bot":
        text = "Who are you, Basel? What is a Career Assistant Bot?";
        break;
      case "search":
        text = "How do you help me find jobs?";
        break;
      case "resume":
        text =
          "Dynamic Resumes? So you can help keep my resume up to date at all times?";
        break;
      case "translations":
        text =
          "Basel, tell me how you can assist in language or technical translation barriers when assisting recruiters and candidates in the job hunt process.";
        break;
      case "candidate":
        text =
          "Hey Basel! I am here to talk with you about the candidate you represent. Can you give me a brief description about this candidate?";
        break;
      case "interview":
        text = `I would love to take the ${context} interview.`;
        break
      default:
        text = "Tell me a bit about the Basel platform.";
    }

    const message: Message = {
      text,
      timestamp: new Date(),
      sender: "user",
    };

    client?.handleSend(message);
  };

  return { handleMessage };
};
