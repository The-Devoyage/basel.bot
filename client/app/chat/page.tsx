"use client";

import { useContext, useEffect } from "react";
import { ChatBody } from "./components";
import { GlobalContext } from "../provider";
import { ChatInput } from "@/shared/chat-input";
import { toggleChatInputFocus } from "@/shared/useStore/chatInput";

export default function Chat() {
  const {
    dispatch,
    store: {
      chatInput: { focused },
    },
  } = useContext(GlobalContext);

  useEffect(() => {
    // Disable scrolling on <html>
    document.documentElement.style.overflow = "hidden";

    dispatch(toggleChatInputFocus(true));

    return () => {
      // Re-enable scrolling when component unmounts
      document.documentElement.style.overflow = "";
    };
  }, [dispatch]);

  return (
    <>
      <section
        className="container mx-auto flex w-full flex-col p-4"
        style={{
          height: focused ? "calc(100vh - 200px)" : "calc(100vh - 148px)",
        }}
      >
        <ChatBody />
      </section>
      <footer className="sticky bottom-0 w-full border-t bg-white dark:border-slate-500 dark:bg-slate-950">
        <ChatInput />
      </footer>
    </>
  );
}
