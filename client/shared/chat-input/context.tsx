"use client";

import {
  Dispatch,
  FC,
  SetStateAction,
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import { Message, File } from "@/types";
import { usePathname, useRouter } from "next/navigation";
import { GlobalContext } from "@/app/provider";

interface ChatInputContext {
  files: File[];
  setFiles: Dispatch<SetStateAction<File[]>>;
  handleAutocomplete: () => string | undefined;
  updateSuggestion: (input: string) => void;
  handleRepeatMessage: (prev: boolean) => void;
  handleMessage: () => void;
  messageText: string;
  setMessageText: Dispatch<SetStateAction<string>>;
  suggestion: string;
}

export const ChatInputContext = createContext<ChatInputContext>({
  files: [],
  setFiles: () => null,
  handleAutocomplete: () => undefined,
  handleRepeatMessage: () => null,
  updateSuggestion: () => null,
  handleMessage: () => null,
  messageText: "",
  setMessageText: () => null,
  suggestion: "",
});

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

export const ChatInputContextProvider: FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [files, setFiles] = useState<File[]>([]);
  const [messageText, setMessageText] = useState<string>("");
  const [suggestion, setSuggestion] = useState<string>("");
  const [repeatedMessage, setRepeatedMessage] = useState<Message | null>(null);
  const router = useRouter();
  const pathname = usePathname();
  const {
    client,
    store: {
      auth: { isAuthenticated },
    },
  } = useContext(GlobalContext);

  useEffect(() => {
    client?.handleConnect();
    return () => client?.handleClose();
  }, [isAuthenticated]);

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
      files,
    };

    client?.handleSend(message);
    setMessageText("");
    setSuggestion("");
    setFiles([]);
    setRepeatedMessage(null);
  };

  const handleRepeatMessage = (previous = true) => {
    if (previous) {
      const messages = client?.messages.filter(
        (m) =>
          m.sender !== "bot" &&
          m.timestamp < (repeatedMessage?.timestamp || new Date()),
      );
      setRepeatedMessage(messages?.at(-1) ?? null);
      setMessageText(messages?.at(-1)?.text || "");
    } else {
      const messages = client?.messages.filter(
        (m) =>
          m.sender !== "bot" &&
          m.timestamp > (repeatedMessage?.timestamp || new Date()),
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

  const value = useMemo(
    () => ({
      files,
      setFiles,
      handleAutocomplete,
      updateSuggestion,
      handleRepeatMessage,
      handleMessage,
      messageText,
      setMessageText,
      suggestion,
    }),
    [files, messageText, suggestion],
  );

  return (
    <ChatInputContext.Provider value={value}>
      {children}
    </ChatInputContext.Provider>
  );
};
