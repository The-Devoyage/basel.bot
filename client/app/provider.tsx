"use client";

import { SocketClient, useSocket } from "@/shared/useSocket";
import { FC, createContext, useEffect, useMemo, useState } from "react";
import { Message, Notification } from "@/types";
import { useVerifyLogin } from "@/shared/useVerifyLogin";
import { useStore } from "@/shared/useStore";
import { setShareableLink, setMe } from "@/shared/useStore/auth";
import { Endpoint } from "@/api";
import { useSearchParams } from "next/navigation";
import { useCallApi } from "@/shared/useCallApi";
import LogRocket from "logrocket";

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
  const interviewAssessmentUuid = searchParams.get("interview_assessment_uuid");
  const [logRocketInitalized, setLogRocketInitalized] = useState(false);
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

  useEffect(() => {
    const env = process.env.NODE_ENV;
    if (env === "production") {
      if (!logRocketInitalized) {
        LogRocket.init("sqlyqw/basel");
        setLogRocketInitalized(true);
      }
      if (store.auth.me && logRocketInitalized) {
        LogRocket.identify(store.auth.me?.uuid, {
          name: store.auth.me.full_name,
          email: store.auth.me.email,
        });
      }
    }
  }, [store.auth.me, logRocketInitalized]);

  const getEndpoint = () => {
    if (slToken) {
      return `?sl_token=${slToken}`;
    } else if (interviewAssessmentUuid) {
      return `?interview_assessment_uuid=${interviewAssessmentUuid}`;
    }
    return "";
  };

  const client = useSocket<Message, Message>(
    `${process.env.NEXT_PUBLIC_SOCKET_URL}/ws${getEndpoint()}`,
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
