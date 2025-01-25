"use client";

import { useHandleMessage } from "@/app/components/init-screen/components";
import { GlobalContext } from "@/app/provider";
import { Button, Tooltip } from "flowbite-react";
import { usePathname, useRouter } from "next/navigation";
import { useContext } from "react";
import { BiConversation } from "react-icons/bi";

export const AddInterviewButton = () => {
  const {
    store: {
      auth: { isAuthenticated },
    },
  } = useContext(GlobalContext);
  const { handleMessage } = useHandleMessage();
  const router = useRouter();
  const pathname = usePathname();

  const handleClick = () => {
    if (pathname !== "/") router.push("/");
    handleMessage("create_interview");
  };

  if (!isAuthenticated) return null;

  return (
    <Tooltip content="Create or Take Interview" className="z-50">
      <Button gradientDuoTone="purpleToBlue" outline onClick={handleClick}>
        <BiConversation className="h-5 w-5" />
      </Button>
    </Tooltip>
  );
};
