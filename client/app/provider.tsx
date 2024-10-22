"use client";

import { SocketClient, useSocket } from "@/shared/useSocket";
import { FC, createContext, useMemo, useEffect, useState } from "react";
import { Message } from "@/types";
import { v4 } from "uuid";
import { useVerifyLogin } from "@/shared/useVerifyLogin";
import { useStore } from "@/shared/useStore";
import { useGetUser } from "@/api";

interface GlobalContext {
  token: string | null;
  setToken?: React.Dispatch<React.SetStateAction<string | null>>;
  client: SocketClient<Message, Message> | null;
  store: ReturnType<typeof useStore>[0];
  dispatch: ReturnType<typeof useStore>[1];
}

export const GlobalContext = createContext<GlobalContext>({
  token: null,
  client: null,
  store: { toasts: [], token: null, me: null },
  dispatch: () => {},
});

interface GlobalProviderProps {
  children: React.ReactNode;
}

export const GlobalProvider: FC<GlobalProviderProps> = ({ children }) => {
  const [token, setToken] = useState<string | null>(null);
  const store = useStore();
  useVerifyLogin(store[1], setToken);

  const client = useSocket<Message, Message>(
    `ws://localhost:8000/ws?token=${token}`,
    {
      handleError: (_) => {
        store[1]({
          type: "ADD_TOAST",
          payload: {
            notification: {
              uuid: v4(),
              type: "error",
              description: "An error occurred, please try again later.",
            },
          },
        });
      },
    },
  );

  useEffect(() => {
    const t = window.localStorage.getItem("token");
    setToken(t);

    const handleStorageChange = () => {
      const t = window.localStorage.getItem("token");
      setToken(t);
    };

    window.addEventListener("storage", handleStorageChange);

    return () => {
      window.removeEventListener("storage", handleStorageChange);
    };
  }, []);

  const value = useMemo(
    () => ({ client, store: store[0], token, setToken, dispatch: store[1] }),
    [
      client.socket,
      client.messages,
      client.handleSend,
      client.loading,
      token,
      store[0],
      store[1],
    ],
  );

  return (
    <GlobalContext.Provider value={value}>{children}</GlobalContext.Provider>
  );
};
