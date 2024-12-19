import { Endpoint, callApi } from "@/api";
import { Typography } from "@/shared/typography";
import { Card } from "flowbite-react";

export const ProfileViews = async () => {
  const shareableLinks = await callApi({
    endpoint: Endpoint.ShareableLinks,
    path: null,
    body: null,
    query: { limit: 0 },
  });
  const verify = await callApi({
    endpoint: Endpoint.Verify,
    path: null,
    body: null,
    query: null,
  });

  if (!verify.success) return null;

  return (
    <Card className="border-4 !border-blue-400 text-center">
      <Typography.Heading className="text-2xl">
        Profile Views
      </Typography.Heading>
      <Typography.Heading className="text-3xl">
        {shareableLinks.data?.reduce((prev, next) => {
          prev = prev + next.views;
          return prev;
        }, 0)}
      </Typography.Heading>
    </Card>
  );
};
