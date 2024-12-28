"use client";

import { GlobalContext } from "@/app/provider";
import { Message } from "@/types";
import { useContext } from "react";

export type MessageType =
  | "interviews"
  | "describe_standup"
  | "shareable_links"
  | "resume"
  | "translations"
  | "candidate"
  | "interview"
  | "standup";

export const useHandleMessage = () => {
  const { client } = useContext(GlobalContext);

  const handleMessage = (type: MessageType, modifier?: string) => {
    let text = "";
    switch (type) {
      case "interviews":
        text =
          "I am interested in learning about what Interviews are on the Basel Platform. How do these work?";
        break;
      case "describe_standup":
        text = "Basel, what is a standup and how often should I participate?";
        break;
      case "shareable_links":
        text =
          "What are shareable links and how do they help me share my bot with potential employers/recruiters?";
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
          "Hey Basel! I am here to talk with you about the candidate you represent. Can you give me a summary of this canidate&apos;s profile?";
        break;
      case "interview":
        text = `I would love to take the ${modifier} interview.`;
        break;
      case "standup":
        text = `Can you please help me to log my next standup?`;
        break;
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
