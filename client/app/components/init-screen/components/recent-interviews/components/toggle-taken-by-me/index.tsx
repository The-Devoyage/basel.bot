"use client";

import { ToggleSwitch } from "flowbite-react";
import { useContext } from "react";
import { InterviewsContext } from "../../context";
import { GlobalContext } from "@/app/provider";

export const ToggleTakenByMe = () => {
  const { isTakenByMe, setIsTakenByMe } = useContext(InterviewsContext);
  const {
    store: { isAuthenticated },
  } = useContext(GlobalContext);

  const handleTakenByMe = (checked: boolean) => {
    setIsTakenByMe(checked);
  };

  if (!isAuthenticated) return null;

  return (
    <div className="flex w-full items-center justify-center rounded-md border border-2 border-purple-300 p-2 md:w-1/5">
      <ToggleSwitch
        checked={isTakenByMe}
        onChange={(c) => handleTakenByMe(c)}
        label="Taken by Me"
        color="purple"
      />
    </div>
  );
};
