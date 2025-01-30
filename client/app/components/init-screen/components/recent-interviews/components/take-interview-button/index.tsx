"use client";

import { Button } from "flowbite-react";
import { FC, useContext } from "react";
import { FaLongArrowAltRight } from "react-icons/fa";
import { useHandleMessage } from "../../..";
import { Interview } from "@/types";
import { GlobalContext } from "@/app/provider";
import { useRouter, usePathname } from "next/navigation";

export const TakeInterviewButton: FC<{ interview: Interview }> = ({
  interview,
}) => {
  const {
    store: {
      auth: { shareableLink },
    },
  } = useContext(GlobalContext);
  const router = useRouter();
  const pathname = usePathname();
  const { handleMessage } = useHandleMessage();

  const handleClick = () => {
    if (pathname !== "/") router.push("/");
    const context = `Interview UUID: ${interview.uuid}`;
    return handleMessage(
      shareableLink ? "recruiter_interview" : "interview",
      interview.name,
      context,
    );
  };

  return (
    <Button outline gradientDuoTone="purpleToBlue" onClick={handleClick}>
      <FaLongArrowAltRight className="h-4 w-4" />
    </Button>
  );
};
