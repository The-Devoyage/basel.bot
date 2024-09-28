"use client";

import { useSocket } from "@/shared/useSocket";
import { FC, createContext, useMemo } from "react";

interface GlobalContext {
  client: ReturnType<typeof useSocket>;
}

export const GlobalContext = createContext<GlobalContext>({
  client: { socket: null, messages: [], handleSend: () => {}, loading: true },
});

interface GlobalProviderProps {
  children: React.ReactNode;
}

export const GlobalProvider: FC<GlobalProviderProps> = ({ children }) => {
  const client = useSocket();

  const value = useMemo(
    () => ({ client }),
    [client.socket, client.messages, client.handleSend],
  );

  return (
    <GlobalContext.Provider value={value}>{children}</GlobalContext.Provider>
  );
};
