"use client";

import { Endpoint } from "@/api";
import { Button } from "@/types";
import { Button as FlowbiteButton, useThemeMode } from "flowbite-react";
import { useRouter } from "next/navigation";
import { FC, useState } from "react";

export const FooterButtons: FC<{ buttons?: Button[] }> = ({ buttons }) => {
  const [loading, setLoading] = useState<number[]>([]);
  const themeMode = useThemeMode();
  const router = useRouter();
  if (!buttons?.length) return null;

  //TODO: This is most likely going to be broken.
  const handleCallAction = async (endpoint: Endpoint) => {
    switch (endpoint) {
      case Endpoint.SubscribeStart:
        return router.push("https://www.basel.bot/pricing");
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
      case "redirect":
        router.push(action.endpoint);
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
          size="sm"
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
