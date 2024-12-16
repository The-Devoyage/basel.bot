"use client";

import { GlobalContext } from "@/app/provider";
import { Progress, Toast } from "flowbite-react";
import { useContext, useEffect, useState } from "react";
import { Typography } from "../typography";
import { removeToast } from "../useStore/toast";

export interface Notification {
  uuid: string;
  type: "error" | "success";
  title?: string;
  description: string;
}

export const Toaster = () => {
  const [hovering, setHovering] = useState<Notification["uuid"][]>([]);
  const {
    store: { toasts },
    dispatch,
  } = useContext(GlobalContext);

  useEffect(() => {
    if (toasts.length === 0) return;

    const activeToast = toasts[0];
    if (!hovering.includes(activeToast.uuid)) {
      const timeout = setTimeout(() => {
        dispatch(removeToast(activeToast));
      }, 3000);

      return () => clearTimeout(timeout);
    }
  }, [toasts, hovering, dispatch]);

  return (
    <div className="fixed right-4 top-4 space-y-4" style={{ zIndex: 999 }}>
      {toasts.map((toast) => (
        <Toast
          key={toast.uuid}
          className={`border-2 border-${toast.type === "error" ? "red" : "green"}-300 flex flex-col items-start`}
          onMouseEnter={() => setHovering((curr) => [...curr, toast.uuid])}
          onMouseLeave={() =>
            setHovering((curr) => curr.filter((u) => u !== toast.uuid))
          }
        >
          <div className="flex">
            <div>
              <Typography.Heading className="mb-1">
                {toast?.title ?? toast.type === "error" ? "Error" : "Success"}
              </Typography.Heading>
              <Typography.Paragraph className="text-sm">
                {toast.description}
              </Typography.Paragraph>
            </div>
            <Toast.Toggle />
          </div>
        </Toast>
      ))}
    </div>
  );
};
