"use client";

import { GlobalContext } from "@/app/provider";
import { Button, Tooltip } from "flowbite-react";
import { useContext } from "react";
import { BiConversation } from "react-icons/bi";
import { useHandleMessage } from "../../..";

export const AddInterviewButton = () => {
  const {
    store: {
      auth: { isAuthenticated },
    },
  } = useContext(GlobalContext);
  const { handleMessage } = useHandleMessage();

  const handleClick = () => {
    handleMessage("create_interview");
  };

  if (!isAuthenticated) return null;

  return (
    <Tooltip content="Create or Take Interview">
      <Button gradientDuoTone="purpleToBlue" outline onClick={handleClick}>
        <BiConversation className="h-5 w-5" />
      </Button>
    </Tooltip>
  );
};
