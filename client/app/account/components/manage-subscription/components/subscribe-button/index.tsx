"use client";

import { Button } from "flowbite-react";
import Link from "next/link";
import { FC } from "react";

interface SubscribeButtonProps {
  hasSubscribed: boolean;
}

export const SubscribeButton: FC<SubscribeButtonProps> = ({
  hasSubscribed,
}) => {
  if (!process.env.NEXT_PUBLIC_BILLING_PORTAL_URL) {
    throw Error(`REQUIRED ENV NOT SET: NEXT_PUBLIC_BILLING_PORTAL_URL`);
  }

  if (hasSubscribed) {
    return (
      <Link href={process.env.NEXT_PUBLIC_BILLING_PORTAL_URL} target="_blank">
        <Button outline gradientDuoTone="purpleToPink">
          Manage Subscription
        </Button>
      </Link>
    );
  }

  return (
    <Button
      outline
      gradientDuoTone="greenToBlue"
      href="https://www.basel.bot/pricing"
    >
      Plans and Pricing
    </Button>
  );
};
