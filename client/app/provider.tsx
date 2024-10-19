"use client";

import { SocketClient, useSocket } from "@/shared/useSocket";
import {
  FC,
  createContext,
  useMemo,
  useEffect,
  useReducer,
  useState,
} from "react";
import { Message } from "@/types";
import { Notification } from "@/shared/toaster";
import { v4 } from "uuid";

interface GlobalContext {
  token: string | null;
  client: SocketClient<Message, Message> | null;
  toasts: Notification[];
  dispatch: React.Dispatch<{
    type: "ADD_TOAST" | "REMOVE_TOAST";
    payload: Notification;
  }> | null;
}

export const GlobalContext = createContext<GlobalContext>({
  token: null,
  client: null,
  toasts: [],
  dispatch: null,
});

interface GlobalProviderProps {
  children: React.ReactNode;
}

export const GlobalProvider: FC<GlobalProviderProps> = ({ children }) => {
  const [token, setToken] = useState<string | null>(null);
  const [{ toasts }, dispatch] = useReducer(
    (
      state: { toasts: Notification[] },
      action: { type: string; payload: Notification },
    ) => {
      switch (action.type) {
        case "ADD_TOAST":
          return {
            ...state,
            toasts: [...state.toasts, action.payload], // Correctly update the `toasts` array
          };
        case "REMOVE_TOAST":
          return {
            ...state,
            toasts: state.toasts.filter(
              (toast) => toast.uuid !== action.payload.uuid, // Filter the toasts array
            ),
          };
        default:
          return state; // Return the current state if action type is unknown
      }
    },
    { toasts: [] },
  );
  const client = useSocket<Message, Message>(
    `ws://localhost:8000/ws?token=${token}`,
    {
      handleError: (_) => {
        dispatch({
          type: "ADD_TOAST",
          payload: {
            uuid: v4(),
            type: "error",
            description: "An error occurred, please try again later.",
          },
        });
      },
    },
  );

  useEffect(() => {
    const t = window.localStorage.getItem("token");
    setToken(t);
  }, []);

  const value = useMemo(
    () => ({ client, toasts, dispatch, token }),
    [
      client.socket,
      client.messages,
      client.handleSend,
      client.loading,
      toasts,
      dispatch,
      token,
    ],
  );

  return (
    <GlobalContext.Provider value={value}>{children}</GlobalContext.Provider>
  );
};
