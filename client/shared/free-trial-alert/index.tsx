"use client";

import { useState } from "react";
import { GlobalContext } from "@/app/provider";
import { Alert } from "flowbite-react";
import { useContext } from "react";
import dayjs from "dayjs";
import Link from "next/link";

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
    <Alert color="green" rounded={false}>
      <span>
        🕰️ Free Trial Alert! You have {daysLeft} days left in your free trial.
        Keep full access by
        <Link href="/account" className="ml-2 font-bold text-green-700 ">
          subscribing today!
        </Link>
        <Link
          className="ml-2 cursor-pointer underline"
          onClick={() => setShow(false)}
          href="#"
        >
          close
        </Link>
      </span>
    </Alert>
  );
};
