"use client";

import { useContext, useEffect, useRef } from "react";
import { GlobalContext } from "@/app/provider";
import { ChatCard } from "@/shared/chat-card";
import { Loader } from "@/shared/loader";
import { Alert, Avatar, Card } from "flowbite-react";
import { Typography } from "@/shared/typography";
import clsx from "clsx";
import { AuthButton } from "@/shared/auth-button";

export const ChatBody = () => {
  const {
    client,
    store: {
      auth: { me, shareableLink, isAuthenticated },
    },
  } = useContext(GlobalContext);
  const ref = useRef<HTMLDivElement>(null);
  const candidate = shareableLink?.user || null;
  const chattingWith = candidate || null || me;
  const linkStatus = shareableLink?.status;

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

  if (!client) return <Loader />;

  if (!client.messages.length) return null;

  return (
    <div className="mx-auto flex w-full flex-col items-end gap-2 md:flex-row">
      <div className="mx-full order-2 flex w-full flex-col justify-center space-y-4 md:order-1 md:min-w-[700px]">
        {client.messages.map((m, index) => (
          <ChatCard
            key={m.timestamp?.toString()}
            message={m}
            ref={index === client?.messages.length - 1 ? ref : undefined}
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
      <div className="static order-1 w-full md:sticky md:bottom-24">
        <Card
          className={clsx("w-full text-center", {
            "border-4 border-red-200": linkStatus === false,
          })}
        >
          <div className="flex flex-col items-center justify-center gap-4">
            <Avatar
              alt="User Avatar"
              size="lg"
              rounded
              placeholderInitials={
                chattingWith?.first_name?.at(0)?.toUpperCase() ||
                chattingWith?.email.at(0)?.toUpperCase()
              }
              bordered
              color="success"
              img={chattingWith?.profile_image?.url}
              theme={{
                root: {
                  img: {
                    on: "flex items-center justify-center object-cover",
                  },
                },
              }}
            />
            {linkStatus === false && (
              <Alert color="failure">Access Revoked</Alert>
            )}
            {chattingWith?.full_name ? (
              <Typography.Heading className="w-2/3 text-xl">
                {chattingWith?.full_name?.trim()}
              </Typography.Heading>
            ) : (
              <Typography.Heading className="w-2/3 text-wrap">
                {chattingWith?.email.split("@")?.at(0) || "Welcome!"}
              </Typography.Heading>
            )}
            {!isAuthenticated && !shareableLink && <AuthButton />}
          </div>
        </Card>
      </div>
    </div>
  );
};
