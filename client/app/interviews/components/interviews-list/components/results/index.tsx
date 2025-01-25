"use client";

import { GlobalContext } from "@/app/provider";
import { InterviewCard } from "@/shared/interview-card";
import { Loader } from "@/shared/loader";
import { Typography } from "@/shared/typography";
import { Interview } from "@/types";
import { Card } from "flowbite-react";
import { FC, useContext } from "react";

export const InterviewListResults: FC<{
  loading: boolean;
  interviews: Interview[];
}> = ({ loading, interviews }) => {
  const {
    store: {
      auth: { isAuthenticated },
    },
  } = useContext(GlobalContext);
  if (loading)
    return (
      <div className="rounded border-2 border-purple-400 p-6">
        <Loader />
      </div>
    );

  if (!interviews.length) {
    return (
      <Card>
        <Typography.Heading className="text-xl">
          Nothing Found!
        </Typography.Heading>
        <Typography.Paragraph>
          Try a different search or create an interview.
        </Typography.Paragraph>
      </Card>
    );
  }

  return (
    <div className="grid w-full grid-cols-1 gap-4 md:grid-cols-3">
      {interviews.map((interview) => (
        <InterviewCard
          key={interview.uuid}
          interview={interview}
          showStatusBadge={!!isAuthenticated}
        />
      ))}
    </div>
  );
};
