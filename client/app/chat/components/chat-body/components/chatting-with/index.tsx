"use client";

import clsx from "clsx";
import { Alert, Card } from "flowbite-react";
import { DisplayName, RecruiterButtons, UserAvatar } from "..";
import { AuthButton } from "@/shared/auth-button";
import { GlobalContext } from "@/app/provider";
import { useContext } from "react";

export const ChattingWith = () => {
  const { store } = useContext(GlobalContext);
  const {
    auth: { me, shareableLink, isAuthenticated },
    interviewAssessment: { assessment },
  } = store;
  const candidate = shareableLink?.user || assessment?.user || null;
  const chattingWith = candidate || me;
  const linkStatus = shareableLink?.status;

  return (
    <>
      <Card
        className={clsx("w-full text-center", {
          "border-4 border-red-200": linkStatus === false,
        })}
      >
        <div className="flex flex-col items-center justify-center gap-4">
          <UserAvatar chattingWith={chattingWith} />
          {linkStatus === false && (
            <Alert color="failure">Access Revoked</Alert>
          )}
          <DisplayName chattingWith={chattingWith} />
          {!isAuthenticated && !shareableLink && <AuthButton isButton />}
        </div>
      </Card>
      <RecruiterButtons />
    </>
  );
};
