"use client";

import { Typography } from "@/shared/typography";
import { Alert, Button } from "flowbite-react";
import { MessageType } from "../..";
import { FC } from "react";
import { Endpoint } from "@/api";
import { useCallApi } from "@/shared/useCallApi";
import clsx from "clsx";

interface RecruiterWelcomeProps {
  handleMessage: (type: MessageType) => void;
  slToken: string | null;
}

export const RecruiterWelcome: FC<RecruiterWelcomeProps> = ({
  handleMessage,
  slToken,
}) => {
  const { res } = useCallApi(
    {
      endpoint: Endpoint.ShareableLink,
      path: {
        sl_token: slToken!,
      },
      body: null,
      query: {
        extend: "user",
      },
    },
    {
      callOnMount: !!slToken,
    },
  );
  const shareableLink = res?.data;
  const status = !!shareableLink?.status;

  if (!slToken || !shareableLink) return null;

  return (
    <Alert
      color={shareableLink.status ? "green" : "failure"}
      className={clsx("w-full space-y-4 border-2", {
        "border-green-600": status,
        "border-red-600": !status,
      })}
    >
      <Typography.Heading className="text-xl dark:!text-slate-800">
        {status ? "Welcome!" : "Access Revoked"}
      </Typography.Heading>
      <Typography.Paragraph className="my-2 dark:text-slate-600">
        {status
          ? `It looks like you might be here to learn about a candidate! Tell Basel
        about yourself, the organization you are with, and the position you are
        trying to fill.`
          : `The user has revoked access to their bot. Please try again later.`}
      </Typography.Paragraph>
      {status && (
        <>
          <Typography.Paragraph className="dark:text-slate-600">
            Basel will help you learn about this candidate so that you may
            determine if they are a good fit or not.
          </Typography.Paragraph>
          <Button
            gradientDuoTone="purpleToBlue"
            outline
            onClick={() => handleMessage("candidate")}
            className="mt-4 w-full"
          >
            Start Interview
          </Button>
        </>
      )}
    </Alert>
  );
};
