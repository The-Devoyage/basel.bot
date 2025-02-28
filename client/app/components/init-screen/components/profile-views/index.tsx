"use client";

import { GlobalContext } from "@/app/provider";
import { Typography } from "@/shared/typography";
import { ShareableLink } from "@/types";
import { Card } from "flowbite-react";
import { FC, useContext } from "react";

export const ProfileViews: FC<{ shareableLinks: ShareableLink[] }> = ({
  shareableLinks,
}) => {
  const {
    store: {
      auth: { isAuthenticated },
      interviewAssessment: { assessment },
    },
    slToken,
  } = useContext(GlobalContext);

  if (!isAuthenticated || assessment || slToken) return null;

  return (
    <Card className="border-4 !border-blue-400 text-center">
      <Typography.Heading className="text-2xl">
        Profile Views
      </Typography.Heading>
      <Typography.Heading className="text-3xl">
        {shareableLinks.reduce((prev, next) => {
          prev = prev + next.views;
          return prev;
        }, 0)}
      </Typography.Heading>
    </Card>
  );
};
