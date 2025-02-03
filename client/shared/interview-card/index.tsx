"use client";

import { Interview } from "@/types";
import { Badge, Card, Tooltip } from "flowbite-react";
import { Typography } from "../typography";
import { TakeInterviewButton } from "@/app/components/init-screen/components/recent-interviews/components";
import { FC } from "react";
import { StatusBadge } from "./components";
import { useRouter } from "next/navigation";

export const InterviewCard: FC<{
  interview: Interview;
  showStatusBadge: boolean;
}> = ({ interview, showStatusBadge }) => {
  const router = useRouter();

  const handleClick = () => {
    router.push(`/interviews/${interview.uuid}`);
  };

  return (
    <Card
      className="cursor-pointer border-t-4 border-t-purple-200 dark:border-t-purple-400"
      key={interview.uuid}
      onClick={handleClick}
    >
      <div className="h-54 flex h-full flex-col justify-between">
        <div className="flex w-full items-start justify-between">
          <Typography.Heading className="text-xl font-bold">
            {interview.position || interview.name}
          </Typography.Heading>
          {showStatusBadge && <StatusBadge interview={interview} />}
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
          <div onClick={(e) => e.stopPropagation()}>
            <Tooltip content="Ask Basel">
              <TakeInterviewButton interview={interview} />
            </Tooltip>
          </div>
        </div>
      </div>
    </Card>
  );
};
