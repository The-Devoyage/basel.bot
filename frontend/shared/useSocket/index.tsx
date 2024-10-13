"use client";

import { useEffect, useState, useRef } from "react";
import { Message } from "@/types";

interface SocketClient {
  socket: WebSocket | null;
  messages: Message[];
  handleSend: (message: Message) => void;
  loading: boolean;
}

export const useSocket = () => {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [loading, setLoading] = useState(true);
  const hasConnected = useRef(false);
  const [messages, setMessages] = useState<Message[]>([]);

  useEffect(() => {
    if (hasConnected.current) {
      return;
    }

    const ws = new WebSocket("ws://localhost:8000/ws");
    setSocket(ws);

    ws.onopen = (e) => {
      setLoading(false);
      console.log("Connected to server", e);
    };

    ws.onmessage = (message) => {
      setLoading(false);
      console.log(message.data);
      setMessages((prev) => [...prev, JSON.parse(message.data)]);
    };

    ws.onclose = () => {
      console.log("Disconnected from server");
    };

    ws.onerror = (error) => {
      console.error("WebSocket Error:", error);
    };

    hasConnected.current = true;

    return () => {
      if (ws.readyState === ws.OPEN) {
        ws.close();
      }
    };
  }, []);

  const handleSend = (message: Message) => {
    setLoading(true);
    setMessages((prev) => [...prev, message]);
    socket?.send(JSON.stringify(message));
  };

  return { socket, messages, handleSend, loading } as SocketClient;
};
