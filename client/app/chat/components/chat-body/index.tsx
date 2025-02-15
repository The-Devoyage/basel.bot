"use client";

import { useContext } from "react";
import { GlobalContext } from "@/app/provider";
import { Loader } from "@/shared/loader";
import { ChattingWith, ScrollingChat } from "./components";

export const ChatBody = () => {
  const { client } = useContext(GlobalContext);

  if (!client) return <Loader />;

  return (
    <div className="relative top-0 flex size-full flex-col gap-8 md:flex-row">
      <div className="hidden w-full md:block md:w-1/4">
        <ChattingWith />
      </div>
      <ScrollingChat />
    </div>
  );
};
