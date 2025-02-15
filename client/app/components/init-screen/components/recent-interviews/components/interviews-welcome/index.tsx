"use client";

import { GlobalContext } from "@/app/provider";
import { Alert } from "flowbite-react";
import { useContext } from "react";
import { FaCircleCheck } from "react-icons/fa6";

export const InterviewsWelcome = () => {
  const { slToken } = useContext(GlobalContext);
  return (
    <Alert color="purple">
      <div className="flex items-center gap-2">
        <FaCircleCheck className="size-4" />
        {slToken ? (
          <div className="flex-1">
            The user has shared tailored interviews for your review. Explore
            them below to gain insights and evaluate their fit.
          </div>
        ) : (
          <div className="flex-1">
            Interviews are tailored experiences crafted alongside Basel from
            real job postings. They highlight skills, evaluate fit, and create
            meaningful insights for both candidates and recruiters to explore.
          </div>
        )}
      </div>
    </Alert>
  );
};
