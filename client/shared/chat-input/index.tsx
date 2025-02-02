"use client";

import { useContext, useEffect, useRef } from "react";
import { GlobalContext } from "@/app/provider";
import { ActionItems, FilePreviews } from "./components";
import clsx from "clsx";
import { ChatInputContext, ChatInputContextProvider } from "./context";
import { toggleChatInputFocus } from "../useStore/chatInput";

export const ChatInputContents = () => {
  const {
    handleMessage,
    messageText,
    setMessageText,
    suggestion,
    handleAutocomplete,
    handleRepeatMessage,
    updateSuggestion,
  } = useContext(ChatInputContext);
  const {
    client,
    dispatch,
    store: {
      chatInput: { focused },
    },
  } = useContext(GlobalContext);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        containerRef.current &&
        !containerRef.current.contains(event.target as Node)
      ) {
        dispatch(toggleChatInputFocus(false));
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  useEffect(() => {
    if (!inputRef.current) return;
    if (focused) {
      inputRef.current.style.height = "auto";
      inputRef.current.style.height = `${inputRef.current.scrollHeight}px`;
    } else {
      inputRef.current.style.height = "auto";
      // inputRef.current.style.height = `${inputRef.current.scrollHeight}px`;
    }
  }, [messageText, focused]);

  useEffect(() => {
    if (focused) {
      inputRef.current?.focus();
    }
  }, [focused]);

  const handleFocus = () => {
    dispatch(toggleChatInputFocus(document.activeElement === inputRef.current));
    setTimeout(() => {
      document.body.style.height = `${window.innerHeight}px`;
    }, 300);
  };

  return (
    <div
      className="container mx-auto flex w-full flex-col space-y-4 p-4 px-4 dark:bg-slate-950"
      ref={containerRef}
    >
      <FilePreviews />
      <div
        className={clsx("rounded border border-slate-200", {
          "border-green-400": focused,
          flex: !focused,
        })}
      >
        <div className="relative flex w-full items-end">
          {suggestion && (
            <div
              className="pointer-events-none absolute left-0 top-0 h-full w-full overflow-hidden whitespace-pre-wrap text-gray-400 dark:text-gray-600"
              style={{
                padding: "0.5rem 0.75rem",
              }}
            >
              {messageText}
              <span className="ml-2">{suggestion}</span>
            </div>
          )}
          <textarea
            placeholder="Message Basel"
            className="no-scrollbar relative h-full w-full resize-none rounded-t-md border-none bg-transparent ring-transparent dark:bg-slate-950/5 dark:text-white"
            rows={1}
            ref={inputRef}
            style={{
              resize: "none",
              minHeight: 50,
            }}
            onChange={(e) => {
              const value = e.target.value;
              setMessageText(value);
              updateSuggestion(value);
            }}
            onFocus={handleFocus}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey && !client?.loading) {
                e.preventDefault();
                handleMessage();
              } else if (e.key === "Tab" || e.key === "ArrowRight") {
                e.preventDefault();
                const newMessageText = handleAutocomplete();
                if (newMessageText) updateSuggestion(newMessageText);
              } else if (e.key === "ArrowUp") {
                e.preventDefault();
                handleRepeatMessage(true);
              } else if (e.key === "ArrowDown") {
                e.preventDefault();
                handleRepeatMessage(false);
              }
            }}
            value={messageText}
          />
        </div>
        <div
          className="flex items-end justify-end"
          onClick={(e) => e.stopPropagation()}
        >
          <ActionItems
            setMessageText={setMessageText}
            handleMessage={handleMessage}
            messageText={messageText}
            inputRef={inputRef}
          />
        </div>
      </div>
    </div>
  );
};

export const ChatInput = () => {
  return (
    <ChatInputContextProvider>
      <ChatInputContents />
    </ChatInputContextProvider>
  );
};
