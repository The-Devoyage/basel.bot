"use client";

import { useContext, useEffect } from "react";
import { GlobalContext } from "@/app/provider";
import { ChatCard } from "@/shared/chat-card";
import { Loader } from "@/shared/loader";

export const ChatBody = () => {
  const {
    client: { messages, loading },
  } = useContext(GlobalContext);

  useEffect(() => {
    const root = document.getElementById("root");
    root?.scrollTo(0, root.scrollHeight);
  }, [messages]);

  if (loading && !messages.length) {
    return <Loader />;
  }

  return (
    <div className="flex flex-col space-y-4">
      {messages.map((m) => (
        <ChatCard key={m.timestamp?.toString()} message={m} />
      ))}
    </div>
  );
};
