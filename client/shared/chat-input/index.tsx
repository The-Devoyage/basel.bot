"use client";

import { useContext, useState, useEffect, useRef } from "react";
import { Button, Textarea } from "flowbite-react";
import { TbShoppingCartSearch } from "react-icons/tb";
import { GlobalContext } from "@/app/provider";
import { Message } from "@/types";

export const ChatInput = () => {
  const [messageText, setMessageText] = useState<string>("");
  const {
    client,
    store: { token },
  } = useContext(GlobalContext);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const hasConnected = useRef<boolean>(false);
  const [textareaHeight, setTextareaHeight] = useState<number | undefined>(
    undefined,
  );

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
    if (hasConnected.current) return;
    if (!token) return;
    client?.handleConnect();
    hasConnected.current = true;

    return () => {
      client?.handleClose();
      hasConnected.current = false;
    };
  }, [token]);

  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.style.height = "auto";
      inputRef.current.style.height = `${inputRef.current.scrollHeight}px`;
      setTextareaHeight(inputRef.current.scrollHeight);
    }
  }, [messageText]);

  return (
    <div className="container mx-auto flex w-full space-x-4 p-4 px-4 dark:bg-slate-950">
      <Textarea
        placeholder={
          token
            ? "Your last interview starts here..."
            : "Login to start chatting"
        }
        className="w-full focus:border-green-400 focus:ring-green-400 dark:bg-slate-950 dark:text-white"
        disabled={!token}
        color="info"
        theme={{
          colors: {
            info: "border-green-100 focus:border-green-400 focus:ring-green-400",
          },
        }}
        rows={1}
        style={{ resize: "none", height: textareaHeight }}
        ref={inputRef}
        onChange={(e) => setMessageText(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleMessage();
          } else if (e.key === "Enter" && e.shiftKey) {
            setMessageText((prev) => prev + "\n");
          }
        }}
        value={messageText}
      />
      <Button color="green" onClick={handleMessage} disabled={!messageText}>
        <TbShoppingCartSearch className="h-6 w-6" />
      </Button>
    </div>
  );
};
