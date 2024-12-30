"use client";

import { Endpoint } from "@/api";
import { GlobalContext } from "@/app/provider";
import { useCallApi } from "@/shared/useCallApi";
import { toggleNotificationDrawer } from "@/shared/useStore/notification";
import clsx from "clsx";
import { Button } from "flowbite-react";
import { useContext, useEffect } from "react";
import { AiTwotoneNotification } from "react-icons/ai";

export const NotificationToggle = () => {
  const {
    dispatch,
    notificationClient,
    store: {
      notifications: { open },
    },
  } = useContext(GlobalContext);
  const { res, call } = useCallApi(
    {
      endpoint: Endpoint.GetNotifications,
      query: {
        limit: 0,
        read: false,
      },
      body: null,
      path: null,
    },
    {
      callOnMount: true,
    },
  );

  useEffect(() => {
    notificationClient?.handleConnect();

    return () => notificationClient?.handleClose();
  }, []);

  useEffect(() => {
    call();
  }, [notificationClient?.messages]);

  const handleClick = () => {
    dispatch(toggleNotificationDrawer(!open));
  };

  return (
    <Button gradientMonochrome="pink" outline onClick={handleClick}>
      <div className="flex items-center justify-center">
        <AiTwotoneNotification
          className={clsx({
            "mr-2": res?.data?.length,
          })}
        />{" "}
        {res?.data?.length || ""}
      </div>
    </Button>
  );
};
