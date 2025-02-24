"use client";

import { useEffect, useState } from "react";
import { GlobalContext } from "@/app/provider";
import { Alert } from "flowbite-react";
import { useContext } from "react";
import dayjs from "dayjs";
import Link from "next/link";

export const FreeTrialAlert = () => {
  const [show, setShow] = useState(false);
  const {
    store: {
      auth: { me, isAuthenticated },
    },
  } = useContext(GlobalContext);
  const daysLeft = dayjs(
    me?.subscription_status.free_trial_expires || dayjs(),
  ).diff(dayjs(), "day");

  useEffect(() => {
    const freeTrialAlert = localStorage.getItem("freeTrialAlert");
    const recentlyClosed = dayjs().isBefore(
      dayjs(freeTrialAlert).add(1, "day"),
    );
    if (recentlyClosed) {
      return setShow(false);
    }

    if (!show || me?.subscription_status.active || !isAuthenticated) {
      setShow(false);
    } else {
      setShow(true);
    }
  }, []);

  const handleClose = () => {
    localStorage.setItem("freeTrialAlert", new Date().toISOString());
    setShow(false);
  };

  if (!show || me?.subscription_status.active || !isAuthenticated) {
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
          onClick={handleClose}
          href="#"
        >
          close
        </Link>
      </span>
    </Alert>
  );
};
