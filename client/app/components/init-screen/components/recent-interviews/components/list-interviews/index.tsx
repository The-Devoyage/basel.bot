"use client";

import { Loader } from "@/shared/loader";
import { InterviewsContext } from "../../context";
import { useContext } from "react";
import { InterviewCard } from "@/shared/interview-card";

export const ListInterviews = () => {
  const { loading, interviews, isTakenByMe } = useContext(InterviewsContext);

  if (loading) {
    return (
      <div className="rounded border-2 border-purple-400 p-4">
        <Loader />
      </div>
    );
  }

  return (
    <div className="grid w-full grid-cols-1 gap-4 md:grid-cols-3">
      {interviews.map((interview) => (
        <InterviewCard
          key={interview.uuid}
          interview={interview}
          showStatusBadge={isTakenByMe}
        />
      ))}
    </div>
  );
};
