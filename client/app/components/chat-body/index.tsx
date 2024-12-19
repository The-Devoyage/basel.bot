"use client";

import { useContext, useEffect, useRef } from "react";
import { GlobalContext } from "@/app/provider";
import { ChatCard } from "@/shared/chat-card";
import { Loader } from "@/shared/loader";
import { Alert, Spinner } from "flowbite-react";

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
    if (client?.messages.length === 1) {
      const initScreen = document.getElementById("init_screen");
      initScreen?.classList.add("hidden");
    }
  }, [ref.current, client?.messages]);

  if (client?.messages.length && !client.connected) {
    return (
      <Alert color="warning" className="flex space-x-4">
        <Spinner />
        <span className="ml-3">
          We are having trouble connecting, please wait while we try to
          reconnect!
        </span>
      </Alert>
    );
  }

  if (!client || client?.initializing) return <Loader />;

  if (client?.loading && !client?.messages.length) {
    return <Loader />;
  }

  return (
    <div className="mx-full flex flex-col justify-center space-y-4 md:mx-auto md:min-w-[700px]">
      {client.messages.map((m, index) => (
        <ChatCard
          key={m.timestamp?.toString()}
          message={m}
          ref={index === client?.messages.length - 1 ? ref : undefined}
        />
      ))}
      {client.loading && (
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
