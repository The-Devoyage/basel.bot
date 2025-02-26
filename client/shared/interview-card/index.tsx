"use client";

import { Interview, Organization } from "@/types";
import { Badge, Card, Tooltip } from "flowbite-react";
import { Typography } from "../typography";
import { TakeInterviewButton } from "@/app/components/init-screen/components/recent-interviews/components";
import { FC } from "react";
import { StatusBadge } from "./components";
import { useRouter } from "next/navigation";
import { GrOrganization } from "react-icons/gr";
import clsx from "clsx";
import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";
import relativeTime from "dayjs/plugin/relativeTime";

dayjs.extend(utc);
dayjs.extend(relativeTime);

export const InterviewCard: FC<{
  interview: Interview;
  showStatusBadge: boolean;
}> = ({ interview, showStatusBadge }) => {
  const router = useRouter();

  const handleClick = () => {
    router.push(`/interviews/${interview.uuid}`);
  };

  const handleBadgeClick = (organization_slug: Organization["slug"]) => {
    router.push(`/organizations/${organization_slug}`);
  };

  return (
    <Card
      className="cursor-pointer border-t-4 border-t-purple-400 transition-all hover:shadow-xl hover:shadow-purple-500/20 dark:border-t-purple-400"
      key={interview.uuid}
      onClick={handleClick}
    >
      <div className="h-54 flex h-full flex-col justify-between gap-2">
        <div className="flex w-full items-start justify-between">
          <div className="flex flex-col">
            <Typography.Heading className="text-slate-400">
              {dayjs
                .utc(interview.created_at)
                .local()
                .from(dayjs.utc().local())}
            </Typography.Heading>
            <Typography.Heading className="text-xl font-bold">
              {interview.position}
            </Typography.Heading>
          </div>
          {showStatusBadge && <StatusBadge interview={interview} />}
        </div>
        <Typography.Paragraph
          className="h-full overflow-hidden dark:text-slate-300"
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
        <div
          className={clsx(
            "mt-2 flex w-full items-end",
            interview.organization ? "justify-between" : "justify-end",
          )}
        >
          {interview.organization && (
            <Badge
              color="blue"
              role="button"
              className="cursor-pointer hover:ring-2 hover:ring-blue-400"
              onClick={(e) => {
                e.stopPropagation();
                handleBadgeClick(interview.organization!.slug);
              }}
            >
              <div className="flex gap-2 py-1">
                <GrOrganization className="h-4 w-4 text-slate-400 dark:text-slate-700" />
                {interview.organization!.name}
              </div>
            </Badge>
          )}
          <div onClick={(e) => e.stopPropagation()}>
            <Tooltip content="Ask Basel">
              <TakeInterviewButton interview={interview} action="interview" />
            </Tooltip>
          </div>
        </div>
      </div>
    </Card>
  );
};
