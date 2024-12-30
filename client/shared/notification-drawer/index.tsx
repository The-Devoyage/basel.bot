"use client";

import { GlobalContext } from "@/app/provider";
import { Drawer, Timeline } from "flowbite-react";
import { useContext, useEffect } from "react";
import { AiTwotoneNotification } from "react-icons/ai";
import { toggleNotificationDrawer } from "../useStore/notification";
import { useCallApi } from "../useCallApi";
import { Endpoint } from "@/api";
import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";
import { NotificationType } from "@/types";
import { MdMarkEmailUnread } from "react-icons/md";

dayjs.extend(utc);

export const NotificationDrawer = () => {
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
        limit: 10,
        offset: 0,
      },
      body: null,
      path: null,
    },
    {
      callOnMount: true,
    },
  );

  useEffect(() => {
    call();
  }, [notificationClient?.messages]);

  const handleClose = () => {
    dispatch(toggleNotificationDrawer(false));
  };

  const matchTitle = (notificationType: NotificationType) => {
    switch (notificationType) {
      case NotificationType.GENERAL:
        return "General Update";
      case NotificationType.META_ADDED:
        return "Meta Index Added";
      default:
        return "Notification";
    }
  };

  return (
    <Drawer open={open} onClose={handleClose}>
      <Drawer.Header
        titleIcon={() => <AiTwotoneNotification className="mr-2" />}
        title="Notifications"
      />
      <Drawer.Items>
        <Timeline>
          {res?.data?.map((n) => (
            <Timeline.Item>
              <Timeline.Point
                icon={() => <MdMarkEmailUnread />}
                theme={{
                  marker: {
                    icon: {
                      wrapper: `absolute -left-3 flex h-6 w-6 items-center justify-center rounded-full ${n.read ? "bg-slate-200" : "bg-green-200"} ring-8 ring-white ${n.read ? "dark:bg-slate-900" : "dark:bg-green-400"} dark:ring-gray-900`,
                    },
                  },
                }}
              />
              <Timeline.Content>
                <Timeline.Time>
                  {dayjs.utc(n.created_at).local().format("MMM D YYYY h:ma")}
                </Timeline.Time>
                <Timeline.Title>{matchTitle(n.type)}</Timeline.Title>
                <Timeline.Body>{n.text}</Timeline.Body>
              </Timeline.Content>
            </Timeline.Item>
          ))}
        </Timeline>
      </Drawer.Items>
    </Drawer>
  );
};
