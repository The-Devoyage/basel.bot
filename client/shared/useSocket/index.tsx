"use client";

import { useState, useRef, MutableRefObject, useEffect } from "react";
import { usePathname, useRouter, useSearchParams } from "next/navigation";

export interface SocketClient<Send, Receive> {
  socket: MutableRefObject<WebSocket | null>;
  messages: Send[] | Receive[];
  handleSend: (
    message: Send,
    appendMessage?: boolean,
    useSlToken?: boolean,
    redirectToChat?: boolean,
  ) => void;
  handleClose: () => void;
  handleConnect: () => WebSocket;
  loading: boolean;
  initializing: boolean;
  connected: boolean;
  incomingMessage: string;
  handlePrependMessages: (items: Send[] | Receive[]) => void;
}

export const useSocket = <Send, Receive>(
  url: string,
  options?: {
    onReceive?: (s: Receive) => void;
    onError?: (e: Event) => void;
    onClose?: () => void;
    groupBy?: string;
  },
) => {
  const socket = useRef<WebSocket | null>(null);
  const [loading, setLoading] = useState(false);
  const [initializing, setInitializing] = useState(true);
  const [messages, setMessages] = useState<(Send | Receive)[]>([]);
  const [incomingMessage, setIncomingMessage] = useState("");
  const [messageQueue, setMessageQueue] = useState<Send[]>([]);
  const [connected, setConnected] = useState(false);
  const closed = useRef(false);
  const router = useRouter();
  const searchParams = useSearchParams();
  const pathname = usePathname();

  useEffect(() => {
    if (socket.current?.readyState === WebSocket.OPEN) {
      if (messageQueue.length) setLoading(true);
      for (const m of messageQueue) {
        socket?.current?.send(JSON.stringify(m));
      }
      setMessageQueue([]);
    }
  }, [socket.current?.readyState]);

  const handlePrependMessages = (items: Send[] | Receive[]) => {
    setMessages((curr) => [...items, ...curr]);
  };

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

      if (parsed.message_type === "card") {
        setMessages((prev) => [...prev, parsed]);
      } else if (parsed.message_type !== "end" && options?.groupBy) {
        setIncomingMessage((curr) => curr + parsed[options.groupBy as string]);
      } else if (parsed.message_type === "end" && options?.groupBy) {
        setIncomingMessage("");
        setMessages((prev) => [...prev, parsed]);
      } else {
        setMessages((prev) => [...prev, parsed]);
      }

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

  const handleSend = (
    message: Send,
    appendMessage = true,
    useSlToken = true,
    redirectToChat = true,
  ) => {
    if (pathname !== "/chat" && useSlToken && redirectToChat) {
      router.push(`/chat?${searchParams.toString()}`);
    } else if (pathname !== "/chat" && !useSlToken && redirectToChat) {
      router.push("/chat");
    }
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
    incomingMessage,
    handlePrependMessages,
  } as SocketClient<Send, Receive>;
};
