"use client";

import { useContext, useEffect, useRef } from "react";
import { GlobalContext } from "@/app/provider";
import { ChatCard } from "@/shared/chat-card";
import { Loader } from "@/shared/loader";
import { Alert, Card } from "flowbite-react";
import clsx from "clsx";
import { AuthButton } from "@/shared/auth-button";
import { DisplayName, RecruiterButtons, UserAvatar } from "./components";
import { Typography } from "@/shared/typography";
import { BiSolidLeaf } from "react-icons/bi";
import { toggleChatInputFocus } from "@/shared/useStore/chatInput";

export const ChatBody = () => {
  const { client, store, dispatch } = useContext(GlobalContext);
  const {
    auth: { me, shareableLink, isAuthenticated },
  } = store;
  const lastMessage = useRef<HTMLDivElement>(null);
  const chatContainer = useRef<HTMLDivElement>(null);
  const candidate = shareableLink?.user || null;
  const chattingWith = candidate || null || me;
  const linkStatus = shareableLink?.status;

  useEffect(() => {
    if (lastMessage.current && chatContainer.current) {
      const messageTop = lastMessage.current.offsetTop;
      chatContainer.current.scrollTo({
        top: messageTop - chatContainer.current.offsetTop,
        behavior: "smooth",
      });
    }
    if (!client?.messages.length) {
      dispatch(toggleChatInputFocus(true));
    }
  }, [client?.messages.length]);

  if (!client) return <Loader />;

  if (!client.messages.length) {
    return (
      <div className="flex h-full w-full items-center justify-center">
        <Card>
          <div className="flex gap-4">
            <BiSolidLeaf className="h-12 w-12 text-green-400" />
            <div className="flex flex-col gap-2">
              <Typography.Heading className="text-2xl">
                Hello! My name is Basel.
              </Typography.Heading>
              <Typography.Paragraph>
                Whether you're here to network, hire, or share your journey — it
                all starts with a conversation.
              </Typography.Paragraph>
            </div>
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div className="relative top-0 flex h-full w-full flex-col gap-8 md:flex-row">
      <div className="hidden w-full md:block md:w-1/4">
        <Card
          className={clsx("w-full text-center", {
            "border-4 border-red-200": linkStatus === false,
          })}
        >
          <div className="flex flex-col items-center justify-center gap-4">
            <UserAvatar chattingWith={chattingWith} />
            {linkStatus === false && (
              <Alert color="failure">Access Revoked</Alert>
            )}
            <DisplayName chattingWith={chattingWith} />
            {!isAuthenticated && !shareableLink && <AuthButton />}
          </div>
        </Card>
        <RecruiterButtons />
      </div>
      <div
        className="no-scrollbar flex w-full flex-col flex-col gap-4 justify-self-end overflow-y-auto md:w-3/4"
        ref={chatContainer}
      >
        {client.messages.map((m, index) => (
          <ChatCard
            key={m.timestamp?.toString()}
            message={m}
            ref={
              index === client?.messages.length - 1 ? lastMessage : undefined
            }
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
    </div>
  );
};
