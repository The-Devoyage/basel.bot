"use client";

import { useState, useRef, MutableRefObject, useEffect } from "react";

export interface SocketClient<Send, Receive> {
  socket: MutableRefObject<WebSocket | null>;
  messages: Send[] | Receive[];
  handleSend: (message: Send, appendMessage?: boolean) => void;
  handleClose: () => void;
  handleConnect: () => WebSocket;
  loading: boolean;
  initializing: boolean;
  connected: boolean;
}

export const useSocket = <Send, Receive>(
  url: string,
  options?: {
    onReceive?: (s: Receive) => void;
    onError?: (e: Event) => void;
    onClose?: () => void;
  },
) => {
  const socket = useRef<WebSocket | null>(null);
  const [loading, setLoading] = useState(false);
  const [initializing, setInitializing] = useState(true);
  const [messages, setMessages] = useState<(Send | Receive)[]>([]);
  const [messageQueue, setMessageQueue] = useState<Send[]>([]);
  const [connected, setConnected] = useState(false);
  const closed = useRef(false);

  useEffect(() => {
    if (socket.current?.readyState === WebSocket.OPEN) {
      if (messageQueue.length) setLoading(true);
      for (const m of messageQueue) {
        socket?.current?.send(JSON.stringify(m));
      }
      setMessageQueue([]);
    }
  }, [socket.current?.readyState]);

  const handleConnect = () => {
    setInitializing(true);
    const ws = new WebSocket(url);

    ws.onopen = () => {
      setLoading(false);
      setInitializing(false);
      setConnected(true);
    };

    ws.onmessage = (message: { data: Receive }) => {
      setLoading(false);
      const parsed = JSON.parse(message.data as string);
      setMessages((prev) => [...prev, parsed]);
      options?.onReceive?.(parsed);
    };

    ws.onclose = () => {
      setConnected(false);
      options?.onClose?.();
    };

    ws.onerror = (error) => {
      options?.onError?.(error);
    };

    socket.current = ws;

    return ws;
  };

  const handleClose = () => {
    closed.current = true;
    socket?.current?.close();
  };

  const handleSend = (message: Send, appendMessage = true) => {
    if (appendMessage) setMessages((prev) => [...prev, message]);
    if (!connected) {
      setMessageQueue((curr) => [...curr, message]);
      return;
    }
    setLoading(true);
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
    connected,
  } as SocketClient<Send, Receive>;
};
