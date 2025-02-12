"use client";

import { Button } from "flowbite-react";
import { FC, useContext } from "react";
import { FaLongArrowAltRight } from "react-icons/fa";
import { useHandleMessage } from "../../..";
import { Interview } from "@/types";
import { GlobalContext } from "@/app/provider";
import { useRouter, usePathname } from "next/navigation";
import clsx from "clsx";

export const TakeInterviewButton: FC<{
  interview: Interview;
  children?: React.ReactNode;
}> = ({ interview, children }) => {
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
      interview.position,
      context,
    );
  };

  return (
    <Button outline gradientDuoTone="purpleToBlue" onClick={handleClick}>
      {children}
      <FaLongArrowAltRight
        className={clsx("h-5 w-5", {
          "ml-2": !!children,
        })}
      />
    </Button>
  );
};
