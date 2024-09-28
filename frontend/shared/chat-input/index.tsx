"use client";
import { useContext, useState, useEffect, useRef } from "react";
import { Button, Textarea } from "flowbite-react";
import { TbShoppingCartSearch } from "react-icons/tb";
import { GlobalContext } from "@/app/provider";
import { Message } from "@/types";

export const ChatInput = () => {
  const [messageText, setMessageText] = useState<string>("");
  const { handleSend } = useContext(GlobalContext);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const handleMessage = () => {
    const message: Message = {
      text: messageText,
      timestamp: new Date(),
      sender: "user",
    };

    handleSend(message);
    setMessageText("");
  };

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  return (
    <div className="container mx-auto flex w-full space-x-4 p-4 px-4">
      <Textarea
        placeholder="Find, watch, buy."
        className="w-full"
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
