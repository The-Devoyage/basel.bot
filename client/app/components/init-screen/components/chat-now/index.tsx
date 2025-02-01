"use client";

import { Button, useThemeMode } from "flowbite-react";
import { BiSolidLeaf } from "react-icons/bi";
import { useRouter } from "next/navigation";
import { useContext } from "react";
import { GlobalContext } from "@/app/provider";

export const ChatNow = () => {
  const router = useRouter();
  const themeMode = useThemeMode();
  const { slToken } = useContext(GlobalContext);

  if (slToken) return null;

  return (
    <Button
      outline={themeMode.mode === "dark"}
      color="green"
      className="w-full"
      onClick={() => router.push("/chat")}
    >
      <BiSolidLeaf className="mr-2 h-5 w-5 text-green-400" />
      Chat Now
    </Button>
  );
};
