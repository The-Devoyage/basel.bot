"use client";

import { Endpoint } from "@/api";
import { Typography } from "@/shared/typography";
import { useCallApi } from "@/shared/useCallApi";
import { Alert, Button, Tooltip } from "flowbite-react";
import { LuRefreshCcwDot } from "react-icons/lu";

export const ResetIndex = () => {
  const { call, loading } = useCallApi(
    {
      endpoint: Endpoint.ResetIndex,
      method: "POST",
      body: {},
      query: null,
      path: null,
    },
    {
      toast: {
        onSuccess: true,
      },
    },
  );

  return (
    <Alert withBorderAccent color="blue">
      <div className="mb-3 flex justify-between">
        <Typography.Heading className="text-xl dark:!text-slate-800">
          Train Basel
        </Typography.Heading>
        <Tooltip content="Retrain Basel">
          <Button
            outline
            gradientDuoTone="purpleToBlue"
            onClick={call}
            isProcessing={loading}
          >
            <LuRefreshCcwDot />
          </Button>
        </Tooltip>
      </div>
      <Typography.Paragraph className="mt-1 dark:text-slate-600">
        Your index is holds the information that Basel uses to recollect
        information about you. Training syncs your meta into Basel&apos;s
        Memory. Note, this does not delete your user information.
      </Typography.Paragraph>
    </Alert>
  );
};
