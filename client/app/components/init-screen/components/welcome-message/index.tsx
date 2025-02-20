"use client";

import { ChatCard } from "@/shared/chat-card";
import { useContext, useEffect, useState } from "react";
import { candidateMessage, recruiterMessage } from "./message";
import { GlobalContext } from "@/app/provider";

export const WelcomeMessage = () => {
  const [message, setMessage] = useState(candidateMessage);
  const {
    store: {
      auth: { shareableLink },
    },
  } = useContext(GlobalContext);

  useEffect(() => {
    if (shareableLink) {
      setMessage(recruiterMessage);
    } else {
      setMessage(candidateMessage);
    }
  }, [shareableLink]);

  return (
    <ChatCard
      message={{
        text: message,
        sender: "bot",
        timestamp: new Date(),
        message_type: "message",
      }}
    />
  );
};
