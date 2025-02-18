"use client";

import { useState } from "react";
import { GlobalContext } from "@/app/provider";
import { Alert } from "flowbite-react";
import { useContext } from "react";
import dayjs from "dayjs";
import { Typography } from "../typography";

export const FreeTrialAlert = () => {
  const [show, setShow] = useState(true);
  const {
    store: {
      auth: { me },
    },
  } = useContext(GlobalContext);
  const daysLeft = dayjs(
    me?.subscription_status.free_trial_expires || dayjs(),
  ).diff(dayjs(), "day");

  if (!show || me?.subscription_status.active) {
    return null;
  }

  return (
    <Alert color="green">
      <div className="flex">
        🕰️ Free Trial Alert! You have {daysLeft} days left in your free trial.
        Keep full access by{" "}
        <Typography.Link
          href="/account"
          className="ml-2 font-bold text-green-700 "
        >
          subscribing today!
        </Typography.Link>
        <Typography.Link
          className="ml-2 cursor-pointer underline"
          onClick={() => setShow(false)}
        >
          close
        </Typography.Link>
      </div>
    </Alert>
  );
};
