"use client";

import { Button } from "flowbite-react";
import { useHandleMessage } from "../../..";

export const SearchInterviewsButton = () => {
  const { handleMessage } = useHandleMessage();

  const handleClick = () => {
    handleMessage("search_interviews");
  };

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
