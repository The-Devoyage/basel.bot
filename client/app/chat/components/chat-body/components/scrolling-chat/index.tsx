"use client";

import { GlobalContext } from "@/app/provider";
import { ChatCard } from "@/shared/chat-card";
import { Loader } from "@/shared/loader";
import { Typography } from "@/shared/typography";
import { Card } from "flowbite-react";
import { useContext, useEffect, useRef, useState } from "react";
import { BiSolidLeaf } from "react-icons/bi";

export const ScrollingChat = () => {
  const { client } = useContext(GlobalContext);
  const lastMessage = useRef<HTMLDivElement>(null);
  const chatContainer = useRef<HTMLDivElement>(null);
  const [hasScrolled, setHasScrolled] = useState(false);
  const [isAtBottom, setIsAtBottom] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      if (client?.incomingMessage) {
        setHasScrolled(true);
        setIsAtBottom(false);
      }
    };

    if (chatContainer.current) {
      chatContainer.current.addEventListener("wheel", handleScroll);
    }

    return () => {
      if (chatContainer.current) {
        chatContainer.current.removeEventListener("wheel", handleScroll);
      }
    };
  }, [chatContainer.current]);

  useEffect(() => {
    const handleScroll = () => {
      if (!chatContainer.current) return;

      const container = chatContainer.current;
      const isAtBottom =
        container.scrollHeight - container.scrollTop <=
        container.clientHeight + 20;

      if (isAtBottom && hasScrolled) {
        setIsAtBottom(true);
      }
    };

    if (chatContainer.current) {
      chatContainer.current.addEventListener("scroll", handleScroll);
    }

    return () => {
      if (chatContainer.current) {
        chatContainer.current.removeEventListener("scroll", handleScroll);
      }
    };
  }, [chatContainer.current, hasScrolled]);

  useEffect(() => {
    setHasScrolled(false);
    setIsAtBottom(false);
  }, [client?.messages.length]);

  useEffect(() => {
    if (isAtBottom) {
      // follow
      chatContainer?.current?.scrollTo({
        top: chatContainer?.current?.scrollHeight,
        behavior: "smooth",
      });
    } else if (!hasScrolled && lastMessage.current && chatContainer.current) {
      const messageTop = lastMessage.current.offsetTop;
      chatContainer.current.scrollTo({
        top: messageTop - chatContainer.current.offsetTop,
        behavior: "smooth",
      });
    }
  }, [client?.messages.length, client?.incomingMessage]);

  if (!client) return <Loader />;

  if (!client.messages.length) {
    return (
      <div className="flex size-full items-start justify-center">
        <Card>
          <div className="flex gap-4">
            <BiSolidLeaf className="size-12 text-green-400" />
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
          key={index}
          message={m}
          ref={
            !client.incomingMessage && index === client?.messages.length - 1
              ? lastMessage
              : undefined
          }
        />
      ))}
      {(client.loading || client.initializing || client.incomingMessage) && (
        <ChatCard
          message={{
            text: client.incomingMessage,
            sender: "bot",
            timestamp: new Date(),
            message_type: "message",
          }}
          loading={!client.incomingMessage}
          ref={client.incomingMessage ? lastMessage : undefined}
        />
      )}
    </div>
  );
};
