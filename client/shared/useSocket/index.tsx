"use client";

import { useState, useRef, MutableRefObject } from "react";

export interface SocketClient<Send, Receive> {
  socket: MutableRefObject<WebSocket | null>;
  messages: Send[] | Receive[];
  handleSend: (message: Send) => void;
  handleClose: () => void;
  handleConnect: () => void;
  loading: boolean;
  initializing: boolean;
  connected: boolean;
}

export const useSocket = <Send, Receive>(
  url: string,
  options?: {
    handleReceive?: (s: Receive) => void;
    handleError?: (e: Event) => void;
    handleRetryFailed?: () => void;
  },
) => {
  const socket = useRef<WebSocket | null>(null);
  const [loading, setLoading] = useState(false);
  const [initializing, setInitializing] = useState(true);
  const [messages, setMessages] = useState<(Send | Receive)[]>([]);
  const connected = useRef(false);
  const reconnectTimeout = useRef(1000);
  const closed = useRef(false);

  const retryConnection = () => {
    if (closed?.current) return;
    setTimeout(() => {
      options?.handleRetryFailed?.();
      handleConnect();
      reconnectTimeout.current = Math.min(reconnectTimeout.current * 2, 30000); // Exponential backoff up to 30 seconds
    }, reconnectTimeout.current);
  };

  const handleConnect = () => {
    setInitializing(true);
    const ws = new WebSocket(url);

    ws.onopen = (e) => {
      setLoading(false);
      setInitializing(false);
      connected.current = true;
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
      connected.current = false;
      retryConnection();
    };

    ws.onerror = (error) => {
      console.error("WebSocket Error:", error);
      options?.handleError?.(error);
    };

    socket.current = ws;

    return ws;
  };

  const handleClose = () => {
    closed.current = true;
    socket?.current?.close();
  };

  const handleSend = (message: Send) => {
    if (!connected) return;
    setLoading(true);
    setMessages((prev) => [...prev, message]);
    socket?.current?.send(JSON.stringify(message));
  };

  return {
    socket,
    messages,
    handleSend,
    handleClose,
    handleConnect,
    loading,
    initializing,
    connected: connected?.current,
  } as SocketClient<Send, Receive>;
};
