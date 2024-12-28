import { Typography } from "@/shared/typography";
import { Alert } from "flowbite-react";
import { CgToday } from "react-icons/cg";
import { FaCircleCheck } from "react-icons/fa6";
import { StandupHeatmap, StartStandupButton } from "./components";
import { Endpoint, callApi } from "@/api";

export const Standup = async () => {
  const verify = await callApi({
    endpoint: Endpoint.Verify,
    body: null,
    query: null,
    path: null,
  });
  const isAuthenticated = verify.success;

  return (
    <div className="w-full space-y-4 rounded-md border-2 border-yellow-300 bg-yellow-50 p-4 dark:bg-slate-900">
      <div className="flex items-center">
        <Typography.Heading className="flex text-lg">
          <CgToday className="mr-2 text-2xl" />
        </Typography.Heading>
        <div className="flex w-full items-center justify-between">
          <Typography.Heading className="text-xl">Standup</Typography.Heading>
          <StartStandupButton />
        </div>
      </div>
      <Alert color="yellow">
        <div className="flex items-center gap-2">
          <FaCircleCheck />
          Share your journey, and your bot will help to shape your career
          profile.
        </div>
      </Alert>
      {isAuthenticated && (
        <div className="flex h-52 items-center justify-center">
          <StandupHeatmap />
        </div>
      )}
    </div>
  );
};
