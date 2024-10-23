"use client";

import { SocketClient, useSocket } from "@/shared/useSocket";
import { FC, createContext, useMemo, useEffect, useState } from "react";
import { Message } from "@/types";
import { useVerifyLogin } from "@/shared/useVerifyLogin";
import { useStore } from "@/shared/useStore";
import { addToast } from "@/shared/useStore/toast";

interface GlobalContext {
  client: SocketClient<Message, Message> | null;
  store: ReturnType<typeof useStore>[0];
  dispatch: ReturnType<typeof useStore>[1];
}

export const GlobalContext = createContext<GlobalContext>({
  client: null,
  store: { toasts: [], token: null },
  dispatch: () => {},
});

interface GlobalProviderProps {
  children: React.ReactNode;
}

export const GlobalProvider: FC<GlobalProviderProps> = ({ children }) => {
  const [store, dispatch] = useStore();
  useVerifyLogin(store, dispatch);

  const client = useSocket<Message, Message>(
    `ws://localhost:8000/ws?token=${store.token}`,
    {
      handleError: (_) => {
        dispatch(
          addToast({
            type: "error",
            description: "An error occurred, please try again later.",
          }),
        );
      },
    },
  );

  const value = useMemo(
    () => ({ client, store, dispatch }),
    [client.socket, client.messages, client.handleSend, client.loading, store],
  );

  return (
    <GlobalContext.Provider value={value}>{children}</GlobalContext.Provider>
  );
};
