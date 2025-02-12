"use client";

import { GlobalContext } from "@/app/provider";
import {
  Button,
  Card,
  Checkbox,
  Drawer,
  Label,
  Pagination,
  Timeline,
} from "flowbite-react";
import { useContext, useEffect, useState } from "react";
import { AiTwotoneNotification } from "react-icons/ai";
import { toggleNotificationDrawer } from "../useStore/notification";
import { useCallApi } from "../useCallApi";
import { Endpoint } from "@/api";
import { NotificationType } from "@/types";
import { MdMarkEmailUnread } from "react-icons/md";
import { addToast } from "../useStore/toast";
import { usePagination } from "../usePagination";
import { Typography } from "../typography";
import { HiOutlineInbox } from "react-icons/hi";
import { toDate } from "@/utils";

export const NotificationDrawer = () => {
  const { pagination, handlePageChange, handleSetTotal, nextOffset } =
    usePagination();
  const [showUnread, setShowUnread] = useState(true);
  const {
    dispatch,
    notificationClient,
    store: {
      notifications: { open },
      auth: { isAuthenticated },
    },
  } = useContext(GlobalContext);

  const { res, call } = useCallApi(
    {
      endpoint: Endpoint.GetNotifications,
      query: {
        limit: pagination.limit,
        offset: nextOffset,
        read: !showUnread,
      },
      body: null,
      path: null,
    },
    {
      onSuccess: async (res) => {
        handleSetTotal(res?.total);
      },
    },
  );

  useEffect(() => {
    if (!isAuthenticated) return;
    call();
    if (notificationClient?.messages.length) {
      // Dispatch toast on new messages
      const last = notificationClient.messages.at(-1);

      if (last && "type" in last && "text" in last) {
        dispatch(
          addToast({
            type: "success",
            title: matchTitle(last.type),
            description: last.text,
          }),
        );
      }
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
  }, [pagination.currentPage, showUnread]);

  useEffect(() => {
    if (!isAuthenticated) return;
    call();
  }, [open]);

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

  const handleClearAll = () => {
    const uuids = (res?.data || []).filter((n) => !n.read).map((n) => n.uuid);
    if (uuids.length) notificationClient?.handleSend({ uuids });
  };

  const handleRead = (uuid: string) => {
    notificationClient?.handleSend({ uuids: [uuid] });
  };

  return (
    <Drawer open={open} onClose={handleClose} id="notification_drawer">
      <Drawer.Header
        titleIcon={() => <AiTwotoneNotification className="mr-2" />}
        title="Notifications"
      />
      <Drawer.Items className="pl-2">
        <Timeline>
          {!res?.data?.length ? (
            <Card className="mb-2">
              <div className="flex w-full items-center justify-center gap-2">
                <HiOutlineInbox className="text-xl dark:text-white" />
                <Typography.Heading className="text-xl">
                  All caught up!
                </Typography.Heading>
              </div>
            </Card>
          ) : (
            res?.data?.map((n) => (
              <Timeline.Item key={n.uuid}>
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
                  <Timeline.Time>{toDate(n.created_at)}</Timeline.Time>
                  <Timeline.Title>{matchTitle(n.type)}</Timeline.Title>
                  <Timeline.Body className="flex flex-col">
                    {n.text}
                    {showUnread && (
                      <Typography.Link
                        className="cursor-pointer underline dark:text-slate-200"
                        onClick={() => handleRead(n.uuid)}
                      >
                        Mark Read
                      </Typography.Link>
                    )}
                  </Timeline.Body>
                </Timeline.Content>
              </Timeline.Item>
            ))
          )}
        </Timeline>
        <div className="flex items-center justify-center gap-2">
          <Checkbox
            checked={showUnread}
            onChange={() => setShowUnread((curr) => !curr)}
          />
          <Label>Show Unread</Label>
        </div>
        <div className="mb-6 flex justify-center text-center">
          <Pagination
            currentPage={pagination.currentPage}
            totalPages={pagination.totalPages}
            onPageChange={handlePageChange}
            layout="navigation"
            showIcons
          />
        </div>
        {showUnread && (
          <Button className="w-full" outline onClick={handleClearAll}>
            Mark Page Read
          </Button>
        )}
      </Drawer.Items>
    </Drawer>
  );
};
