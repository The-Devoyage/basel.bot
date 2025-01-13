"use client";

import { useContext, useState, useEffect, useRef } from "react";
import { GlobalContext } from "@/app/provider";
import { Message } from "@/types";
import { useRouter, usePathname } from "next/navigation";
import { ChatAutocomplete } from "./components";
import clsx from "clsx";

// Command map with primary commands and subcommands
const commandResponses: Record<string, Record<string, string>> = {
  "/interviews": {
    list: "Can you please list interviews available for me to take?",
    take: "I'd like to take an interview based on a job posting I have found.",
    create:
      "Can you help me create a custom interview that does not have a job posting?",
  },
  "/standup": {
    log: "Can you assist me with logging a new standup?",
    list: "Can you list my recent standups?",
  },
};

export const ChatInput = () => {
  const [messageText, setMessageText] = useState<string>("");
  const [suggestion, setSuggestion] = useState<string>(""); // Current suggestion
  const {
    client,
    store: { isAuthenticated },
  } = useContext(GlobalContext);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const router = useRouter();
  const pathname = usePathname();
  const [repetedMessage, setRepeatedMessage] = useState<Message | null>(null);
  const [isFocused, setIsFocused] = useState(false);

  useEffect(() => {
    client?.handleConnect();
    return () => client?.handleClose();
  }, [isAuthenticated]);

  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.style.height = "auto";
      inputRef.current.style.height = `${inputRef.current.scrollHeight}px`;
    }
  }, [messageText]);

  const handleRepeatMessage = (previous = true) => {
    if (previous) {
      const messages = client?.messages.filter(
        (m) =>
          m.sender !== "bot" &&
          m.timestamp < (repetedMessage?.timestamp || new Date()),
      );
      setRepeatedMessage(messages?.at(-1) ?? null);
      setMessageText(messages?.at(-1)?.text || "");
    } else {
      const messages = client?.messages.filter(
        (m) =>
          m.sender !== "bot" &&
          m.timestamp > (repetedMessage?.timestamp || new Date()),
      );
      setRepeatedMessage(messages?.at(0) ?? null);
      setMessageText(messages?.at(0)?.text || "");
    }
  };

  // Update the suggestion based on the current input
  const updateSuggestion = (input: string) => {
    if (!isAuthenticated) return;
    if (input.split(" ").length > 2) return;
    if (input.startsWith("/")) {
      // Split input to identify the base command and subcommand
      const [baseCommand, subCommand] = input.split(" ");

      // Show primary commands if no base command or incomplete base command is typed
      const primaryCommands = Object.keys(commandResponses).filter((cmd) =>
        cmd.startsWith(input),
      );

      if (primaryCommands.length > 0) {
        setSuggestion(primaryCommands.join(" | "));
      } else {
        setSuggestion("");
      }

      // If base command exists, show subcommands
      const subcommands = commandResponses[baseCommand];
      if (subcommands) {
        const matchingSubcommands = Object.keys(subcommands).filter((cmd) =>
          cmd.startsWith(subCommand || ""),
        );

        const isMatch =
          matchingSubcommands.length === 1 &&
          matchingSubcommands[0] === subCommand;

        if (isMatch) {
          // Stop Suggesting, match complete
          setSuggestion("");
        } else if (matchingSubcommands.length > 0) {
          setSuggestion(matchingSubcommands.join(" | "));
        }
      }
    } else {
      setSuggestion("");
    }
  };

  const handleMessage = () => {
    if (pathname !== "/") router.push("/");
    if (!messageText) return;
    if (!client?.connected) client?.handleConnect();

    // Check if the message is a command and format it accordingly
    const [baseCommand, subCommand] = messageText.split(" ");
    const formattedText =
      commandResponses?.[baseCommand]?.[subCommand] || messageText;

    const message: Message = {
      text: formattedText,
      timestamp: new Date(),
      sender: "user",
    };

    client?.handleSend(message);
    setMessageText("");
    setSuggestion("");
    setRepeatedMessage(null);
  };

  const handleAutocomplete = () => {
    if (suggestion) {
      const firstSuggestion = suggestion.split(" | ")?.at(0);
      const hasBase =
        Object.keys(commandResponses).findIndex((k) =>
          messageText.startsWith(k),
        ) > -1;
      const newMessageText = hasBase
        ? messageText.split(" ")?.at(0) + " " + (firstSuggestion || suggestion)
        : firstSuggestion || suggestion;
      setMessageText(newMessageText);
      setSuggestion("");
      return newMessageText;
    }
  };

  const checkFocus = () => {
    setIsFocused(document.activeElement === inputRef.current);
  };

  return (
    <div className="container mx-auto flex w-full flex-col p-4 px-4 dark:bg-slate-950">
      <div
        className={clsx("rounded border border-slate-200", {
          "border-green-400": isFocused,
          flex: !isFocused,
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
            onFocus={checkFocus}
            onBlur={checkFocus}
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
        <div className="flex items-end justify-end">
          <ChatAutocomplete
            setMessageText={setMessageText}
            handleMessage={handleMessage}
            messageText={messageText}
          />
        </div>
      </div>
    </div>
  );
};
