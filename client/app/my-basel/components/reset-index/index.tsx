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
        Resetting your index allows her to get a fresh start on your data.
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
