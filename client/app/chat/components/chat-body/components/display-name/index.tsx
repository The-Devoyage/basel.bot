"use client";

import { Typography } from "@/shared/typography";
import { User } from "@/types";
import { FC } from "react";

export const DisplayName: FC<{ chattingWith: User | null }> = ({
  chattingWith,
}) => {
  if (chattingWith?.full_name)
    return (
      <Typography.Heading className="w-2/3 text-xl">
        {chattingWith?.full_name?.trim()}
      </Typography.Heading>
    );

  return (
    <Typography.Heading className="w-2/3 text-wrap">
      {chattingWith?.email.split("@")?.at(0) || "Welcome!"}
    </Typography.Heading>
  );
};
