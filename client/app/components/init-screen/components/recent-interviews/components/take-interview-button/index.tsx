"use client";

import { Button, ButtonProps } from "flowbite-react";
import { FC, useContext } from "react";
import { FaLongArrowAltRight } from "react-icons/fa";
import { useHandleMessage } from "../../..";
import { Interview } from "@/types";
import { GlobalContext } from "@/app/provider";
import { useRouter, usePathname } from "next/navigation";
import clsx from "clsx";

interface TakeInterviewButtonProps extends ButtonProps {
  interview: Interview;
  action: "take_interview" | "interview";
  children?: React.ReactNode;
}

export const TakeInterviewButton: FC<TakeInterviewButtonProps> = ({
  interview,
  action,
  children,
  ...props
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
    const context =
      action === "take_interview"
        ? `Interview UUID: ${interview.uuid}. Ask me questions one at a time. Check to see if I have completed any questions and pick up where I left off. Use the ask_interview_question tool to ask questions.`
        : `Interview UUID: ${interview.uuid}`;
    return handleMessage(
      shareableLink ? "recruiter_interview" : action,
      interview.position,
      context,
    );
  };

  return (
    <Button
      outline
      gradientDuoTone="purpleToBlue"
      onClick={handleClick}
      {...props}
    >
      {children}
      <FaLongArrowAltRight
        className={clsx("h-5 w-5", {
          "ml-2": !!children,
        })}
      />
    </Button>
  );
};
