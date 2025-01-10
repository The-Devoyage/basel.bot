import { Endpoint, callApi } from "@/api";
import { Typography } from "@/shared/typography";
import { Avatar, Card } from "flowbite-react";

export const UserWelcome = async () => {
  const res = await callApi({
    endpoint: Endpoint.Me,
    query: null,
    body: null,
    path: null,
  });
  const isAuthenticated = await callApi({
    endpoint: Endpoint.Verify,
    path: null,
    body: null,
    query: null,
  });
  const me = res.data;

  if (!isAuthenticated.success) return null;

  return (
    <Card className="border-4 !border-green-400 text-center">
      <div className="flex items-center justify-center gap-2">
        <Avatar
          alt="User Avatar"
          rounded
          placeholderInitials={
            me?.first_name?.at(0)?.toUpperCase() ||
            me?.email.at(0)?.toUpperCase()
          }
          bordered
          color="success"
        />
        {me?.full_name ? (
          <Typography.Heading>{me?.full_name?.trim()}</Typography.Heading>
        ) : (
          <Typography.Link>Introduce Yourself</Typography.Link>
        )}
      </div>
    </Card>
  );
};
