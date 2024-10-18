"use client";
import { useContext, useState, useEffect, useRef } from "react";
import { Button, Textarea } from "flowbite-react";
import { TbShoppingCartSearch } from "react-icons/tb";
import { GlobalContext } from "@/app/provider";
import { Message } from "@/types";

export const ChatInput = () => {
  const [messageText, setMessageText] = useState<string>("");
  const { client } = useContext(GlobalContext);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const handleMessage = () => {
    if (!messageText) return;
    const message: Message = {
      text: messageText,
      timestamp: new Date(),
      sender: "user",
    };
    client?.handleSend(message);
    setMessageText("");
  };

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  return (
    <div className="container mx-auto flex w-full space-x-4 p-4 px-4 dark:bg-slate-950">
      <Textarea
        placeholder="Your last interview starts here..."
        className="w-full focus:border-green-400 focus:ring-green-400 dark:bg-slate-900 dark:text-white"
        color="info"
        theme={{
          colors: {
            info: "border-green-100 focus:border-green-400 focus:ring-green-400",
          },
        }}
        rows={1}
        ref={inputRef}
        onChange={(e) => setMessageText(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            e.preventDefault();
            handleMessage();
          }
        }}
        value={messageText}
      />
      <Button color="green" onClick={handleMessage}>
        <TbShoppingCartSearch className="h-6 w-6" />
      </Button>
    </div>
  );
};
