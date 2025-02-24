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
  | "take_interview"
  | "interview"
  | "standup"
  | "create_interview"
  | "search_interviews"
  | "summerize_standups"
  | "generate_resume"
  | "recruiter_interview"
  | "create_organization_interview";

export const useHandleMessage = () => {
  const { client } = useContext(GlobalContext);

  const handleMessage = (
    type: MessageType,
    modifier?: string | null,
    context?: string,
  ) => {
    let text = "";
    let useSlToken = true;
    switch (type) {
      case "interviews":
        useSlToken = false;
        text =
          "I am interested in learning about what Interviews are on the Basel Platform. How do these work?";
        break;
      case "describe_standup":
        useSlToken = false;
        text = "Basel, what is a standup and how often should I participate?";
        break;
      case "shareable_links":
        useSlToken = false;
        text =
          "What are shareable links and how do they help me share my bot with potential employers/recruiters?";
        break;
      case "resume":
        text =
          "Dynamic Resumes? So you can help keep my resume up to date at all times?";
        break;
      case "translations":
        useSlToken = false;
        text =
          "Basel, tell me how you can assist in language or technical translation barriers when assisting recruiters and candidates in the job hunt process.";
        break;
      case "candidate":
        text =
          "Hey Basel! I am here to talk with you about the candidate you represent. Can you give me a summary of this candidate&apos;s profile?";
        break;
      case "interview":
        text = `Please tell me about the '${modifier}' interview.`;
        break;
      case "take_interview":
        text = `I&apos;d like to take the '${modifier}' interview.`;
        break;
      case "standup":
        text = `Can you please help me to log my next standup?`;
        break;
      case "create_interview":
        text =
          "I'd love to create a new interview for a posting that I have found.";
        break;
      case "search_interviews":
        text = "Can you please search for interviews that might interest me?";
        break;
      case "summerize_standups":
        text = `Can you please summerize the standups I submitted from ${modifier}.`;
        break;
      case "generate_resume":
        text = `Generate a resume for the candidate.`;
        break;
      case "recruiter_interview":
        text = `Summerize how the candidate responded to the &apos;${modifier}&apos; interview.`;
        break;
      case "create_organization_interview":
        text = `I want to create an interview for my organization.`;
        break;

      default:
        text = "Tell me a bit about the Basel platform.";
    }

    const message: Message = {
      text,
      timestamp: new Date(),
      sender: "user",
      context,
      message_type: "message",
    };

    client?.handleSend(message, true, useSlToken);
  };

  return { handleMessage };
};
