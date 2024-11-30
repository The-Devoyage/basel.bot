"use client";

import { useContext, useState, useEffect, useRef } from "react";
import { Button } from "flowbite-react";
import { GrSend } from "react-icons/gr";
import { GlobalContext } from "@/app/provider";
import { Message } from "@/types";
import { useRouter, usePathname, useSearchParams } from "next/navigation";

// Command map with primary commands and subcommands
const commandResponses: Record<string, Record<string, string>> = {
  "/interviews": {
    list: "Tell me about some interviews I can take.",
    create: "Create a new interview with a name and description.",
  },
};

export const ChatInput = () => {
  const [messageText, setMessageText] = useState<string>("");
  const [suggestion, setSuggestion] = useState<string>(""); // Current suggestion
  const {
    client,
    store: { isAuthenticated },
  } = useContext(GlobalContext);
  const searchParams = useSearchParams();
  const token = searchParams.get("sl_token");
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const router = useRouter();
  const pathname = usePathname();
  const [repetedMessage, setRepeatedMessage] = useState<Message | null>(null);

  useEffect(() => {
    if (inputRef.current && isAuthenticated) inputRef.current?.focus();
  }, [inputRef.current, isAuthenticated]);

  const handleFocus = () => {
    if (client && !client?.connected && (isAuthenticated || token)) {
      client.handleConnect();
    }
  };

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
        } else {
          setSuggestion("joejoe");
        }
      }
    } else {
      setSuggestion("");
    }
  };

  const handleMessage = () => {
    if (pathname !== "/") router.push("/");
    if (!messageText) return;

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

  return (
    <div className="container mx-auto flex w-full space-x-4 p-4 px-4 dark:bg-slate-950">
      <div className="relative w-full">
        <div
          className="pointer-events-none absolute left-0 top-0 h-full w-full overflow-hidden whitespace-pre-wrap text-gray-400 dark:text-gray-600"
          style={{
            padding: "0.5rem 0.75rem",
          }}
        >
          {messageText}
          <span className="ml-2">{suggestion}</span>
        </div>
        <textarea
          placeholder={
            isAuthenticated
              ? "Ask something to get started or type '/' for commands..."
              : "Login to start chatting"
          }
          className="relative h-full w-full resize-none rounded bg-transparent focus:border-green-400 focus:ring-green-400 dark:bg-slate-950/5 dark:text-white"
          rows={1}
          ref={inputRef}
          onChange={(e) => {
            const value = e.target.value;
            setMessageText(value);
            updateSuggestion(value);
          }}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
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
          onFocus={handleFocus}
        />
      </div>
      <Button color="green" onClick={handleMessage} disabled={!messageText}>
        <GrSend className="h-6 w-6" />
      </Button>
    </div>
  );
};
