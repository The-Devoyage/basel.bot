"use client";

import { useContext, useEffect, useRef } from "react";
import { GlobalContext } from "@/app/provider";
import { ChatCard } from "@/shared/chat-card";
import { Loader } from "@/shared/loader";
import { Alert, Spinner } from "flowbite-react";
import { useSearchParams } from "next/navigation";
import { InitScreen } from "./components";

export const ChatBody = () => {
  const {
    client,
    store: { isAuthenticated },
  } = useContext(GlobalContext);
  const ref = useRef<HTMLDivElement>(null);
  const searchParams = useSearchParams();
  const token = searchParams.get("sl_token");

  useEffect(() => {
    if (ref.current) {
      const top = ref.current.getBoundingClientRect().top;
      if (top > 0) {
        window.scrollTo(0, window.scrollY + top - 74);
      }
    }
  }, [ref.current, client?.messages]);

  if (!client?.messages?.length && !client?.initializing) {
    return <InitScreen />;
  }

  if (
    client?.messages.length &&
    !client.connected &&
    (isAuthenticated || token)
  ) {
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

  if ((client?.loading && !client?.messages.length) || client?.initializing) {
    return <Loader />;
  }

  return (
    <div className="mx-auto flex flex-col space-y-4">
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
