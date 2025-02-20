"use client";

import { SocketClient, useSocket } from "@/shared/useSocket";
import { FC, createContext, useEffect, useMemo } from "react";
import { Message, Notification } from "@/types";
import { useVerifyLogin } from "@/shared/useVerifyLogin";
import { useStore } from "@/shared/useStore";
import { setShareableLink, setMe } from "@/shared/useStore/auth";
import { Endpoint } from "@/api";
import { useSearchParams } from "next/navigation";
import { useCallApi } from "@/shared/useCallApi";

interface GlobalContext {
  client: SocketClient<Message, Message> | null;
  notificationClient: SocketClient<{ uuids: string[] }, Notification> | null;
  store: ReturnType<typeof useStore>[0];
  dispatch: ReturnType<typeof useStore>[1];
  slToken: string | null;
}

export const GlobalContext = createContext<GlobalContext>({
  client: null,
  store: {
    toasts: [],
    auth: {
      isAuthenticated: null,
      me: null,
      shareableLink: null,
    },
    notifications: { open: false },
    chatInput: { focused: false },
  },
  dispatch: () => {},
  slToken: null,
  notificationClient: null,
});

interface GlobalProviderProps {
  children: React.ReactNode;
}

export const GlobalProvider: FC<GlobalProviderProps> = ({ children }) => {
  const [store, dispatch] = useStore();
  const searchParams = useSearchParams();
  const slToken = searchParams.get("sl_token");
  useVerifyLogin(dispatch);
  const { call } = useCallApi(
    {
      endpoint: Endpoint.Me,
      query: null,
      body: null,
      path: null,
    },
    {
      onSuccess: (res) => {
        if (res.data) dispatch(setMe(res.data));
      },
    },
  );
  useCallApi(
    {
      endpoint: Endpoint.ShareableLink,
      path: {
        sl_token: slToken!,
      },
      body: null,
      query: null,
    },
    {
      callOnMount: !!slToken,
      onSuccess: (res) => {
        if (res.data) dispatch(setShareableLink(res.data));
      },
    },
  );

  useEffect(() => {
    if (store.auth.isAuthenticated) call();
  }, [store.auth.isAuthenticated]);

  const client = useSocket<Message, Message>(
    `${process.env.NEXT_PUBLIC_SOCKET_URL}/ws${slToken ? "?sl_token=" + slToken : ""}`,
    {
      groupBy: "text",
    },
  );
  const notificationClient = useSocket<{ uuids: string[] }, Notification>(
    `${process.env.NEXT_PUBLIC_SOCKET_URL}/notification`,
  );

  const value = useMemo(
    () => ({ client, store, dispatch, slToken, notificationClient }),
    [client, store, slToken, dispatch, notificationClient],
  );

  return (
    <GlobalContext.Provider value={value}>{children}</GlobalContext.Provider>
  );
};
