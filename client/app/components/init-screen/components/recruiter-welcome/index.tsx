"use client";

import { Typography } from "@/shared/typography";
import { Alert, Button } from "flowbite-react";
import { useContext } from "react";
import { Endpoint } from "@/api";
import { useCallApi } from "@/shared/useCallApi";
import clsx from "clsx";
import { useHandleMessage } from "..";
import { GlobalContext } from "@/app/provider";

export const RecruiterWelcome = () => {
  const { slToken } = useContext(GlobalContext);
  const { handleMessage } = useHandleMessage();
  const { res } = useCallApi(
    {
      endpoint: Endpoint.ShareableLink,
      path: {
        sl_token: slToken!,
      },
      body: null,
      query: null,
    },
    {
      callOnMount: !!slToken,
    },
  );
  const shareableLink = res?.data;
  const user = shareableLink?.user;
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
          ? `It looks like you might be here to learn about ${user?.first_name || "a candidate"}.`
          : `The user has revoked access to their bot. Please try again later.`}
      </Typography.Paragraph>
      {status && (
        <>
          <Typography.Paragraph className="dark:text-slate-600">
            Ask me anything you&apos;d like to know about the candidate, and
            I&apos;ll do my best to answer on their behalf.
          </Typography.Paragraph>
          <div className="flex gap-2">
            <Button
              gradientDuoTone="greenToBlue"
              outline
              onClick={() =>
                handleMessage(
                  "generate_resume",
                  null,
                  "Only provide information that has been supplied by the candidate.",
                )
              }
              className="mt-4 w-full"
            >
              Resume
            </Button>
            <Button
              gradientDuoTone="purpleToBlue"
              outline
              onClick={() => handleMessage("candidate")}
              className="mt-4 w-full"
            >
              Interview
            </Button>
          </div>
        </>
      )}
    </Alert>
  );
};
