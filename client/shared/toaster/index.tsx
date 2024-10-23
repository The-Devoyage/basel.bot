"use client";

import { GlobalContext } from "@/app/provider";
import { Toast } from "flowbite-react";
import { useContext, useEffect } from "react";
import { Typography } from "../typography";
import { removeToast } from "../useStore/toast";

export interface Notification {
  uuid: string;
  type: "error" | "success";
  title?: string;
  description: string;
}

export const Toaster = () => {
  const {
    store: { toasts },
    dispatch,
  } = useContext(GlobalContext);

  useEffect(() => {
    const timeout = setTimeout(() => {
      dispatch(removeToast(toasts[0]));
    }, 3000);

    return () => clearTimeout(timeout);
  }, [toasts]);

  return (
    <div className="fixed right-4 top-4 space-y-4" style={{ zIndex: 999 }}>
      {toasts.map((toast) => (
        <Toast
          key={toast.uuid}
          className={`bg-${toast.type === "error" ? "red" : "green"}-100 flex flex-col items-start`}
        >
          <Typography.Heading className="mb-1">
            {toast?.title ?? toast.type === "error" ? "Error" : "Success"}
          </Typography.Heading>
          <Typography.Paragraph className="text-sm">
            {toast.description}
          </Typography.Paragraph>
        </Toast>
      ))}
    </div>
  );
};
