"use client";

import { Endpoint } from "@/api";
import { useCallApi } from "@/shared/useCallApi";
import { Button } from "flowbite-react";
import Link from "next/link";
import { FC } from "react";

interface SubscribeButtonProps {
  hasSubscribed: boolean;
}

export const SubscribeButton: FC<SubscribeButtonProps> = ({
  hasSubscribed,
}) => {
  const { call, loading } = useCallApi({
    endpoint: Endpoint.SubscribeStart,
    body: null,
    path: null,
    query: null,
  });

  const handleSubscribe = async () => {
    const res = await call();
    if (res?.success) {
      window.open(res.data?.url);
    }
  };

  if (!process.env.NEXT_PUBLIC_BILLING_PORTAL_URL) {
    throw Error(`REQUIRED ENV NOT SET: NEXT_PUBLIC_BILLING_PORTAL_URL`);
  }

  if (hasSubscribed) {
    return (
      <Link href={process.env.NEXT_PUBLIC_BILLING_PORTAL_URL} target="_blank">
        <Button outline gradientDuoTone="greenToBlue">
          Manage Subscription
        </Button>
      </Link>
    );
  }

  return (
    <Button
      outline
      gradientDuoTone="greenToBlue"
      isProcessing={loading}
      onClick={handleSubscribe}
    >
      Subscribe - $3.99/mo
    </Button>
  );
};
