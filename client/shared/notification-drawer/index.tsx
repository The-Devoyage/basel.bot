"use client";

import { GlobalContext } from "@/app/provider";
import { Drawer, Pagination, Timeline } from "flowbite-react";
import { useContext, useEffect } from "react";
import { AiTwotoneNotification } from "react-icons/ai";
import { toggleNotificationDrawer } from "../useStore/notification";
import { useCallApi } from "../useCallApi";
import { Endpoint } from "@/api";
import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";
import { NotificationType, Notification } from "@/types";
import { MdMarkEmailUnread } from "react-icons/md";
import { addToast } from "../useStore/toast";
import { usePagination } from "../usePagination";

dayjs.extend(utc);

export const NotificationDrawer = () => {
  const { pagination, handlePageChange, handleSetTotal, nextOffset } =
    usePagination();
  const {
    dispatch,
    notificationClient,
    store: {
      notifications: { open },
      isAuthenticated,
    },
  } = useContext(GlobalContext);

  const { res, call } = useCallApi(
    {
      endpoint: Endpoint.GetNotifications,
      query: {
        limit: pagination.limit,
        offset: nextOffset,
      },
      body: null,
      path: null,
    },
    {
      callOnMount: true,
      onSuccess: async (res) => {
        handleSetTotal(res?.total);

        // Mark messages as read when user has seen them
        const uuids = (res.data || [])
          .filter((n) => !n.read)
          .map((n) => n.uuid);
        if (uuids.length) notificationClient?.handleSend({ uuids }, false);
      },
    },
  );

  useEffect(() => {
    if (!isAuthenticated) return;
    call();
    if (notificationClient?.messages.length) {
      // Dispatch toast on new messages
      const last = notificationClient.messages.at(-1) as Notification;
      dispatch(
        addToast({
          type: "success",
          title: last.type,
          description: last.text,
        }),
      );
    }
  }, [notificationClient?.messages.length]);

  useEffect(() => {
    if (!isAuthenticated) return;
    call();
    const notificationDrawer = window.document.getElementById(
      "notification_drawer",
    );

    if (notificationDrawer) {
      notificationDrawer.scrollTo({ top: 0, behavior: "smooth" });
    }
  }, [pagination.currentPage]);

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
    <Drawer open={open} onClose={handleClose} id="notification_drawer">
      <Drawer.Header
        titleIcon={() => <AiTwotoneNotification className="mr-2" />}
        title="Notifications"
      />
      <Drawer.Items className="pl-2">
        <Timeline>
          {res?.data?.map((n) => (
            <Timeline.Item>
              <Timeline.Point
                icon={() => <MdMarkEmailUnread />}
                theme={{
                  marker: {
                    icon: {
                      wrapper: `absolute -left-3 flex h-6 w-6 items-center justify-center rounded-full ${n.read ? "bg-slate-200" : "bg-green-200"} ring-8 ring-white ${n.read ? "dark:bg-slate-400" : "dark:bg-green-400"} dark:ring-gray-900`,
                    },
                  },
                }}
              />
              <Timeline.Content>
                <Timeline.Time>
                  {dayjs.utc(n.created_at).local().format("MMM D YYYY h:mma")}
                </Timeline.Time>
                <Timeline.Title>{matchTitle(n.type)}</Timeline.Title>
                <Timeline.Body>{n.text}</Timeline.Body>
              </Timeline.Content>
            </Timeline.Item>
          ))}
        </Timeline>
        <div className="mb-6 flex justify-center text-center">
          <Pagination
            currentPage={pagination.currentPage}
            totalPages={pagination.totalPages}
            onPageChange={handlePageChange}
            layout="navigation"
            showIcons
          />
        </div>
      </Drawer.Items>
    </Drawer>
  );
};
