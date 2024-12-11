"use client";

import { Endpoint } from "@/api";
import { Typography } from "@/shared/typography";
import { useCallApi } from "@/shared/useCallApi";
import { Alert, Button } from "flowbite-react";

export const ResetIndex = () => {
  const { call, loading } = useCallApi({
    endpoint: Endpoint.ResetIndex,
    method: "POST",
    body: {},
    query: null,
    path: null,
  });

  return (
    <Alert withBorderAccent color="failure">
      <Typography.Heading className="text-xl dark:!text-slate-800">
        Reset Index
      </Typography.Heading>
      <Typography.Paragraph className="mt-1 dark:text-slate-600">
        Your index is holds the information that Basel uses to recollect.
        Resetting your index allows Basel to get a fresh take. Note, this does
        not delete your user information.
      </Typography.Paragraph>
      <Button
        outline
        color="failure"
        onClick={call}
        isProcessing={loading}
        className="mt-3"
      >
        Reset Index
      </Button>
    </Alert>
  );
};
