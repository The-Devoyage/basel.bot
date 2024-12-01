"use client";

import { GlobalContext } from "@/app/provider";
import { ChatCard } from "@/shared/chat-card";
import { Message } from "@/types";
import { Button } from "flowbite-react";
import { useContext } from "react";

export const InitScreen = () => {
  const { client } = useContext(GlobalContext);

  const handleMessage = (type: "interviews" | "bot" | "search" | "resume") => {
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
  return (
    <div className="mx-auto flex h-full flex-col items-center justify-center space-y-4">
      <ChatCard
        message={{
          text: `Hello there! I'm Basel, your personal career assistant. I am 
                   ready to help you find jobs, prepare for interviews, and keep 
                   your dynamic resume up to date. **How can I help you today?**`,
          sender: "bot",
          timestamp: new Date(),
        }}
      />
      <Button.Group>
        <Button
          gradientDuoTone="greenToBlue"
          outline
          onClick={() => handleMessage("interviews")}
        >
          Automated Interviews
        </Button>
        <Button
          gradientDuoTone="greenToBlue"
          outline
          onClick={() => handleMessage("bot")}
        >
          Personalized Bot
        </Button>
        <Button
          gradientDuoTone="greenToBlue"
          outline
          onClick={() => handleMessage("search")}
        >
          Job Search
        </Button>
        <Button
          gradientDuoTone="greenToBlue"
          outline
          onClick={() => handleMessage("resume")}
        >
          Dynamic Resumes
        </Button>
      </Button.Group>
    </div>
  );
};
