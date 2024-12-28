"use client";

import { Button } from "flowbite-react";
import { FC, useContext } from "react";
import { FaLongArrowAltRight } from "react-icons/fa";
import { useHandleMessage } from "../../..";
import { Interview } from "@/types";
import { GlobalContext } from "@/app/provider";

export const TakeInterviewButton: FC<{ interview: Interview }> = ({
  interview,
}) => {
  const {
    store: { isAuthenticated },
  } = useContext(GlobalContext);
  const { handleMessage } = useHandleMessage();

  const handleClick = () => {
    return handleMessage("interview", interview.name);
  };

  if (!isAuthenticated) return null;

  return (
    <Button outline gradientDuoTone="purpleToBlue" onClick={handleClick}>
      <FaLongArrowAltRight className="h-4 w-4" />
    </Button>
  );
};
