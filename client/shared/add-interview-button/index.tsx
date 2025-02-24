"use client";

import { useHandleMessage } from "@/app/components/init-screen/components";
import { GlobalContext } from "@/app/provider";
import { SubscriptionFeature } from "@/types";
import { useCheckPerm } from "@/utils/useCheckPerm";
import { Button, Tooltip } from "flowbite-react";
import { usePathname, useRouter } from "next/navigation";
import { useContext } from "react";
import { BiConversation } from "react-icons/bi";

export const AddInterviewButton = () => {
  const {
    store: {
      auth: { isAuthenticated },
    },
  } = useContext(GlobalContext);
  const allowCreate = useCheckPerm(SubscriptionFeature.CREATE_INTERVIEW);
  const { handleMessage } = useHandleMessage();
  const router = useRouter();
  const pathname = usePathname();

  const handleClick = () => {
    if (pathname !== "/") router.push("/");
    handleMessage(
      "create_interview",
      null,
      "Do not attach organization. I'll provide a URL; Scrape it to create the interview.",
    );
  };

  if (!isAuthenticated) return null;

  return (
    <Tooltip
      content={
        allowCreate
          ? "Create or Take Interview"
          : "Upgrade membership to create mock interviews."
      }
      className="z-50"
    >
      <Button
        gradientDuoTone="purpleToBlue"
        outline
        onClick={handleClick}
        disabled={!allowCreate}
      >
        <BiConversation className="h-5 w-5" />
      </Button>
    </Tooltip>
  );
};
