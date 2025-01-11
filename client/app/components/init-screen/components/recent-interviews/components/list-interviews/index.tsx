"use client";

import { Typography } from "@/shared/typography";
import { TakeInterviewButton } from "..";
import { Loader } from "@/shared/loader";
import { InterviewsContext } from "../../context";
import { useContext } from "react";
import { Badge, Card, Tooltip } from "flowbite-react";
import { StatusBadge } from "./components";

export const ListInterviews = () => {
  const { loading, interviews, isTakenByMe } = useContext(InterviewsContext);

  if (loading) {
    return (
      <div className="rounded border border-2 border-purple-400 p-4">
        <Loader />
      </div>
    );
  }

  return (
    <div className="grid w-full grid-cols-1 gap-4 md:grid-cols-3">
      {interviews.map((interview) => (
        <Card
          className="border-t-4 border-t-purple-200 dark:border-t-purple-400"
          key={interview.uuid}
        >
          <div className="h-54 flex h-full flex-col justify-between">
            <div className="flex w-full items-start justify-between">
              <Typography.Heading className="text-xl font-bold">
                {interview.position || interview.name}
              </Typography.Heading>
              {isTakenByMe && <StatusBadge interview={interview} />}
            </div>
            <Typography.Heading className="italic">
              {interview.position && interview.name}
            </Typography.Heading>
            <Typography.Paragraph
              className="h-full overflow-hidden"
              style={{
                display: "-webkit-box",
                WebkitBoxOrient: "vertical",
                WebkitLineClamp: 5,
                lineHeight: "1.5",
                maxHeight: "calc(1.5em * 5)",
              }}
            >
              {interview.description}
            </Typography.Paragraph>
            <div className="mt-2 flex w-full items-end justify-between">
              <Badge color="green">{interview.organization_name}</Badge>
              <Tooltip content="Learn More">
                <TakeInterviewButton interview={interview} />
              </Tooltip>
            </div>
          </div>
        </Card>
      ))}
    </div>
  );
};
