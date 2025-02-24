"use client";

import { Typography } from "@/shared/typography";
import { Card } from "flowbite-react";
import { useContext } from "react";
import { InterviewPageContext } from "../../context";

export const InterviewDescription = () => {
  const { interview } = useContext(InterviewPageContext);

  if (!interview) return null;

  return (
    <Card className="w-full">
      <Typography.Heading className="text-2xl">
        Interview Description
      </Typography.Heading>
      <Typography.Paragraph>{interview.description}</Typography.Paragraph>
    </Card>
  );
};
