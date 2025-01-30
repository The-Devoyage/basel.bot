"use client";

import { GlobalContext } from "@/app/provider";
import { Typography } from "@/shared/typography";
import { Avatar, Card } from "flowbite-react";
import { useContext } from "react";

export const UserWelcome = () => {
  const {
    store: {
      auth: { me, shareableLink },
    },
  } = useContext(GlobalContext);
  const candidate = shareableLink?.user || null || me;

  if (!candidate) return null;

  return (
    <Card className="border-4 !border-green-400 text-center">
      <div className="flex flex-col items-center justify-center gap-4">
        <Avatar
          alt="User Avatar"
          size="lg"
          rounded
          placeholderInitials={
            candidate?.first_name?.at(0)?.toUpperCase() ||
            candidate?.email.at(0)?.toUpperCase()
          }
          bordered
          color="success"
          img={candidate?.profile_image?.url}
          theme={{
            root: {
              img: {
                on: "flex items-center justify-center object-cover",
              },
            },
          }}
        />
        {candidate?.full_name ? (
          <Typography.Heading className="w-2/3 text-xl">
            {candidate?.full_name?.trim()}
          </Typography.Heading>
        ) : (
          <Typography.Heading>Welcome!</Typography.Heading>
        )}
      </div>
    </Card>
  );
};
