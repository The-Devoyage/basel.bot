"use client";

import { useEffect, useState, useRef } from "react";
import { Message } from "@/types";

export const useSocket = () => {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const hasConnected = useRef(false);
  const [messages, setMessages] = useState<Message[]>([]);

  useEffect(() => {
    if (hasConnected.current) {
      return;
    }

    const ws = new WebSocket("ws://localhost:8765");
    setSocket(ws);

    ws.onopen = (e) => {
      console.log("Connected to server", e);
    };

    ws.onmessage = (message) => {
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
    setMessages((prev) => [...prev, message]);
    socket?.send(JSON.stringify(message));
  };

  return { socket, messages, handleSend };
};
