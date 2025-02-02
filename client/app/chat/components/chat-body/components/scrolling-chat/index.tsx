"use client";

import { GlobalContext } from "@/app/provider";
import { ChatCard } from "@/shared/chat-card";
import { Loader } from "@/shared/loader";
import { Typography } from "@/shared/typography";
import { Card } from "flowbite-react";
import { useContext, useEffect, useRef } from "react";
import { BiSolidLeaf } from "react-icons/bi";

export const ScrollingChat = () => {
  const { client } = useContext(GlobalContext);
  const lastMessage = useRef<HTMLDivElement>(null);
  const chatContainer = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (lastMessage.current && chatContainer.current) {
      const messageTop = lastMessage.current.offsetTop;
      chatContainer.current.scrollTo({
        top: messageTop - chatContainer.current.offsetTop,
        behavior: "smooth",
      });
    }
  }, [client?.messages.length]);

  if (!client) return <Loader />;

  if (!client.messages.length) {
    return (
      <div className="flex h-full w-full items-start justify-center">
        <Card>
          <div className="flex gap-4">
            <BiSolidLeaf className="h-12 w-12 text-green-400" />
            <div className="flex flex-col gap-2">
              <Typography.Heading className="text-2xl">
                Hello! My name is Basel.
              </Typography.Heading>
              <Typography.Paragraph>
                Whether you&apos;re here to network, hire, or share your journey
                — it all starts with a conversation.
              </Typography.Paragraph>
            </div>
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div
      className="no-scrollbar flex w-full flex-col flex-col gap-4 overflow-y-auto"
      ref={chatContainer}
    >
      {client.messages.map((m, index) => (
        <ChatCard
          key={m.timestamp?.toString()}
          message={m}
          ref={index === client?.messages.length - 1 ? lastMessage : undefined}
        />
      ))}
      {(client.loading || client.initializing) && (
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
