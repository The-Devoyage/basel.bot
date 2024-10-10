"use client";

import { useContext, useEffect, useRef } from "react";
import { GlobalContext } from "@/app/provider";
import { ChatCard } from "@/shared/chat-card";
import { Loader } from "@/shared/loader";

export const ChatBody = () => {
  const {
    client: { messages, loading },
  } = useContext(GlobalContext);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (ref.current) {
      const top = ref.current.getBoundingClientRect().top;
      console.log(top);
      if (top > 0) {
        window.scrollTo(0, window.scrollY + top - 74);
      }
    }
  }, [ref.current, messages]);

  if (loading && !messages.length) {
    return <Loader />;
  }

  return (
    <div className="flex flex-col space-y-4">
      {messages.map((m, index) => (
        <ChatCard
          key={m.timestamp?.toString()}
          message={m}
          ref={index === messages.length - 1 ? ref : undefined}
        />
      ))}
      {loading && <Loader />}
    </div>
  );
};
