"use client";

import { Loader } from "@/shared/loader";
import { InterviewsContext } from "../../context";
import { useContext } from "react";
import { InterviewCard } from "@/shared/interview-card";
import { GlobalContext } from "@/app/provider";
import { Card } from "flowbite-react";
import { Typography } from "@/shared/typography";

export const ListInterviews = () => {
  const { slToken } = useContext(GlobalContext);
  const { loading, interviews, isTakenByMe } = useContext(InterviewsContext);

  if (loading) {
    return (
      <div className="rounded border-2 border-purple-400 p-4">
        <Loader />
      </div>
    );
  }

  if (!interviews.length) {
    return (
      <Card>
        <Typography.Heading className="text-xl">
          No Interviews Found
        </Typography.Heading>
        <Typography.Paragraph>
          {!slToken
            ? "It looks like there are no interviews available at the moment."
            : "The candidate has not attached any interviews to this link."}
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
          showStatusBadge={!!slToken || isTakenByMe}
        />
      ))}
    </div>
  );
};
