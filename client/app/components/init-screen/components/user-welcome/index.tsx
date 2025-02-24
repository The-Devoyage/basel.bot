"use client";

import { GlobalContext } from "@/app/provider";
import { Typography } from "@/shared/typography";
import { Avatar, Card } from "flowbite-react";
import { useContext } from "react";
import { BiSolidLeaf } from "react-icons/bi";

export const UserWelcome = () => {
  const {
    store: {
      auth: { me, shareableLink },
    },
  } = useContext(GlobalContext);
  const candidate = shareableLink?.user || null || me;

  if (!candidate) {
    return (
      <Card className="border-4 !border-green-400 text-center">
        <div className="flex flex-col items-center justify-center gap-4">
          <BiSolidLeaf className="size-12 text-green-400" />
          <Typography.Heading>Hey, I&apos;m Basel!</Typography.Heading>
        </div>
      </Card>
    );
  }

  return (
    <Card className="border-4 !border-green-400 text-center">
      <div className="flex flex-col items-center justify-center gap-4">
        <Avatar
          alt="User Avatar"
          size="lg"
          rounded
          placeholderInitials={candidate?.first_initial}
          bordered
          color="success"
          img={candidate?.profile_image?.url}
          theme={{
            root: {
              img: {
                on: "flex items-center justify-center object-cover",
                placeholder: "mt-6 text-gray-400",
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
