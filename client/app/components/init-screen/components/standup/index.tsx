import { Typography } from "@/shared/typography";
import { Alert } from "flowbite-react";
import { CgToday } from "react-icons/cg";
import { FaCircleCheck } from "react-icons/fa6";
import { StartStandupButton } from "./components";

export const Standup = () => {
  return (
    <div className="w-full space-y-4 rounded-md border-2 border-yellow-300 p-4">
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
    </div>
  );
};
