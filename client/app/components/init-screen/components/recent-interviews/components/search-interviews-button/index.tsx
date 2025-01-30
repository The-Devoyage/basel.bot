"use client";

import { Button } from "flowbite-react";
import { useHandleMessage } from "../../..";
import { useContext } from "react";
import { GlobalContext } from "@/app/provider";

export const SearchInterviewsButton = () => {
  const { handleMessage } = useHandleMessage();
  const {
    store: {
      auth: { shareableLink },
    },
  } = useContext(GlobalContext);

  const handleClick = () => {
    handleMessage("search_interviews");
  };

  if (shareableLink) return null;

  return (
    <Button
      outline
      gradientDuoTone="purpleToBlue"
      className="w-full"
      onClick={handleClick}
    >
      Search Interviews
    </Button>
  );
};
