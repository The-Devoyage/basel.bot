"use client";

import { useSocket } from "@/shared/useSocket";
import { FC, createContext, useMemo } from "react";
import { Message } from "@/types";

interface GlobalContext {
  socket: WebSocket | null;
  messages: Message[];
  handleSend: (message: Message) => void;
}

export const GlobalContext = createContext<GlobalContext>({
  socket: null,
  messages: [],
  handleSend: () => {},
});

interface GlobalProviderProps {
  children: React.ReactNode;
}

export const GlobalProvider: FC<GlobalProviderProps> = ({ children }) => {
  const { socket, messages, handleSend } = useSocket();

  const value = useMemo(
    () => ({ socket, messages, handleSend }),
    [socket, messages],
  );

  return (
    <GlobalContext.Provider value={value}>{children}</GlobalContext.Provider>
  );
};
