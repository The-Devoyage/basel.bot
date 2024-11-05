"use client";

import { useEffect, useState } from "react";

export interface SocketClient<Send, Receive> {
  socket: WebSocket | null;
  messages: Send[] | Receive[];
  handleSend: (message: Send) => void;
  handleClose: () => void;
  handleConnect: () => Promise<void>;
  loading: boolean;
  initializing: boolean;
  connected: boolean;
}

export const useSocket = <Send, Receive>(
  url: string,
  options?: {
    handleReceive?: (s: Receive) => void;
    handleError?: (e: Event) => void;
  },
) => {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [loading, setLoading] = useState(false);
  const [initializing, setInitializing] = useState(false);
  const [messages, setMessages] = useState<(Send | Receive)[]>([]);
  const [connected, setConnected] = useState(false);

  console.log("URL ", url);

  if (!url) {
    throw new Error("URL is required");
  }

  const handleConnect = async () => {
    setInitializing(true);
    const ws = new WebSocket(url);
    setSocket(ws);

    ws.onopen = (e) => {
      setLoading(false);
      setInitializing(false);
      setConnected(true);
      console.log("Connected to server", e);
    };

    ws.onmessage = (message: { data: Receive }) => {
      setLoading(false);
      const parsed = JSON.parse(message.data as string);
      setMessages((prev) => [...prev, parsed]);
      options?.handleReceive?.(parsed);
    };

    ws.onclose = () => {
      console.log("Disconnected from server");
      setConnected(false);
    };

    ws.onerror = (error) => {
      console.error("WebSocket Error:", error);
      options?.handleError?.(error);
    };
  };

  const handleClose = () => {
    if (connected) {
      socket?.close();
    }
  };

  const handleSend = (message: Send) => {
    setLoading(true);
    setMessages((prev) => [...prev, message]);
    socket?.send(JSON.stringify(message));
  };

  return {
    socket,
    messages,
    handleSend,
    handleClose,
    handleConnect,
    loading,
    initializing,
    connected,
  } as SocketClient<Send, Receive>;
};
