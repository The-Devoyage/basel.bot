"use client";
import { Typography } from "@/shared/typography";
import { Alert } from "flowbite-react";
import { CgToday } from "react-icons/cg";
import { FaCircleCheck } from "react-icons/fa6";
import { StandupHeatmap, StartStandupButton } from "./components";
import { useContext } from "react";
import { GlobalContext } from "@/app/provider";

export const Standup = () => {
  const {
    store: {
      auth: { isAuthenticated, shareableLink },
    },
  } = useContext(GlobalContext);

  return (
    <div className="w-full space-y-4 rounded-md border-2 border-yellow-300 bg-yellow-50 p-4 dark:bg-slate-900">
      <div className="flex items-center">
        <Typography.Heading className="flex text-lg">
          <CgToday className="mr-2 text-2xl" />
        </Typography.Heading>
        <div className="flex w-full items-center justify-between">
          <Typography.Heading className="text-xl">Standups</Typography.Heading>
          <StartStandupButton />
        </div>
      </div>
      <Alert color="yellow">
        <div className="flex items-center gap-2">
          <FaCircleCheck className="h-4 w-4" />
          <div className="flex-1">
            Standups capture daily progress—what’s been accomplished, current
            focus, and challenges. These updates build a dynamic career profile,
            shining a spotlight on growth, dedication, and the journey every
            step of the way.
          </div>
        </div>
      </Alert>
      {(isAuthenticated || shareableLink) && (
        <div className="flex h-52 items-center justify-center">
          <StandupHeatmap />
        </div>
      )}
    </div>
  );
};
