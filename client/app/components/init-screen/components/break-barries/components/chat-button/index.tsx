"use client";

import { Button } from "flowbite-react";
import { useHandleMessage } from "../../..";

export const ChatButton = () => {
  const { handleMessage } = useHandleMessage();

  return (
    <Button
      gradientDuoTone="greenToBlue"
      className="mt-4 w-full"
      onClick={() => handleMessage("translations")}
    >
      Start Chatting
    </Button>
  );
};
