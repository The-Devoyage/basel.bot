"use client";

import { useContext, useState, useEffect, useRef } from "react";
import { Button, Textarea } from "flowbite-react";
import { TbShoppingCartSearch } from "react-icons/tb";
import { GlobalContext } from "@/app/provider";
import { Message } from "@/types";
import { useRouter, usePathname } from "next/navigation";

export const ChatInput = () => {
  const [messageText, setMessageText] = useState<string>("");
  const {
    client,
    store: { isAuthenticated },
  } = useContext(GlobalContext);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const hasConnected = useRef<boolean>(false);
  const [textareaHeight, setTextareaHeight] = useState<number | undefined>(
    undefined,
  );
  const router = useRouter();
  const pathname = usePathname();

  const handleMessage = () => {
    if (pathname !== "/") router.push("/");
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
    if (inputRef.current) inputRef.current?.focus();
  }, [inputRef.current]);

  useEffect(() => {
    if (hasConnected.current) return;
    if (!isAuthenticated) return;
    client?.handleConnect();
    hasConnected.current = true;

    return () => {
      client?.handleClose();
      hasConnected.current = false;
    };
  }, [isAuthenticated]);

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
          isAuthenticated
            ? "Ask something to get started..."
            : "Login to start chatting"
        }
        className="w-full focus:border-green-400 focus:ring-green-400 dark:bg-slate-950 dark:text-white"
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
