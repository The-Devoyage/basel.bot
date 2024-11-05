"use client";

import { SocketClient, useSocket } from "@/shared/useSocket";
import { FC, createContext, useEffect, useMemo } from "react";
import { Message } from "@/types";
import { useVerifyLogin } from "@/shared/useVerifyLogin";
import { useStore } from "@/shared/useStore";
import { addToast } from "@/shared/useStore/toast";
import { setMe } from "@/shared/useStore/auth";
import { Endpoint, callApi } from "@/api";
import { useSearchParams } from "next/navigation";

interface GlobalContext {
  client: SocketClient<Message, Message> | null;
  store: ReturnType<typeof useStore>[0];
  dispatch: ReturnType<typeof useStore>[1];
}

export const GlobalContext = createContext<GlobalContext>({
  client: null,
  store: { toasts: [], isAuthenticated: false, me: null },
  dispatch: () => {},
});

interface GlobalProviderProps {
  children: React.ReactNode;
}

export const GlobalProvider: FC<GlobalProviderProps> = ({ children }) => {
  const [store, dispatch] = useStore();
  const searchParams = useSearchParams();
  const token = searchParams.get("sl_token");
  useVerifyLogin(dispatch);

  const client = useSocket<Message, Message>(
    `${process.env.NEXT_PUBLIC_SOCKET_URL}/ws${token ? "?sl_token=" + token : ""}`,
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

  useEffect(() => {
    if (!store.isAuthenticated || store.me) return;

    const handleFetchMe = async () => {
      try {
        const me = await callApi({
          endpoint: Endpoint.Me,
          query: null,
          body: null,
          path: null,
        });
        if (!me.success || !me.data) {
          throw new Error("Failed to fetch user.");
        }
        dispatch(setMe(me.data));
      } catch (error) {
        console.error(error);
        dispatch(
          addToast({
            type: "error",
            description: "An error occurred while fetching user.",
          }),
        );
      }
    };

    handleFetchMe();
  }, [store.isAuthenticated]);

  const value = useMemo(
    () => ({ client, store, dispatch }),
    [client.socket, client.messages, client.handleSend, client.loading, store],
  );

  return (
    <GlobalContext.Provider value={value}>{children}</GlobalContext.Provider>
  );
};
