"use client";

import { Endpoint } from "@/api";
import { useCallApi } from "@/shared/useCallApi";
import { Button } from "@/types";
import { Button as FlowbiteButton, useThemeMode } from "flowbite-react";
import { FC, useState } from "react";

export const FooterButtons: FC<{ buttons?: Button[] }> = ({ buttons }) => {
  const [loading, setLoading] = useState<number[]>([]);
  const themeMode = useThemeMode();
  const { call: handleSubscribe } = useCallApi(
    {
      endpoint: Endpoint.SubscribeStart,
      body: null,
      query: null,
      path: null,
    },
    {
      onSuccess: (res) => {
        window.open(res.data?.url);
      },
    },
  );
  if (!buttons?.length) return null;

  const handleCallAction = async (endpoint: Endpoint) => {
    switch (endpoint) {
      case Endpoint.SubscribeStart:
        await handleSubscribe();
      default:
        return;
    }
  };

  const handleAction = async (action: Button["action"], index: number) => {
    setLoading((curr) => [...curr, index]);
    switch (action.type) {
      case "call":
        await handleCallAction(action.endpoint);
        setLoading((curr) => curr.filter((i) => i !== index));
        break;
      default:
        return;
    }
  };

  return (
    <div className="flex justify-end space-x-2">
      {buttons.map((b, index) => (
        <FlowbiteButton
          key={index}
          color="green"
          outline={themeMode.mode === "dark"}
          isProcessing={loading.includes(index)}
          onClick={() => handleAction(b.action, index)}
        >
          {b.label}
        </FlowbiteButton>
      ))}
    </div>
  );
};
