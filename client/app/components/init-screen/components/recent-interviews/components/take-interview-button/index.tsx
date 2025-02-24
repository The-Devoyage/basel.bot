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
  action: "take_interview" | "interview";
  children?: React.ReactNode;
}> = ({ interview, action, children }) => {
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
    const context =
      action === "take_interview"
        ? `Interview UUID: ${interview.uuid}. Ask me questions one at a time. Check to see if I have completed any questions and pick up where I left off.`
        : `Interview UUID: ${interview.uuid}`;
    return handleMessage(
      shareableLink ? "recruiter_interview" : action,
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
