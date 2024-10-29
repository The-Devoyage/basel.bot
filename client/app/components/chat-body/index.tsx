"use client";

import { useContext, useEffect, useRef } from "react";
import { GlobalContext } from "@/app/provider";
import { ChatCard } from "@/shared/chat-card";
import { Loader } from "@/shared/loader";

export const ChatBody = () => {
  const { client } = useContext(GlobalContext);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (ref.current) {
      const top = ref.current.getBoundingClientRect().top;
      if (top > 0) {
        window.scrollTo(0, window.scrollY + top - 74);
      }
    }
  }, [ref.current, client?.messages]);

  if (!client?.messages?.length && !client?.initializing) {
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
      </div>
    );
  }

  if ((client?.loading && !client?.messages.length) || client?.initializing) {
    return <Loader />;
  }

  return (
    <div className="mx-auto flex w-full flex-col space-y-4">
      {client?.messages.map((m, index) => (
        <ChatCard
          key={m.timestamp?.toString()}
          message={m}
          ref={index === client?.messages.length - 1 ? ref : undefined}
        />
      ))}
      {client?.loading && (
        <ChatCard
          message={{
            text: "",
            sender: "bot",
            timestamp: new Date(),
          }}
          loading
        />
      )}
    </div>
  );
};
