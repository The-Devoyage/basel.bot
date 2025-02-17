"use client";
import { Endpoint } from "@/api";
import { GlobalContext } from "@/app/provider";
import { useCallApi } from "@/shared/useCallApi";
import { SubscriptionTier } from "@/types";
import { Alert, Button } from "flowbite-react";
import { redirect, useRouter, useSearchParams } from "next/navigation";
import { useContext, useEffect, useState } from "react";

export const CheckoutButton = () => {
  const [disabled, setDisabled] = useState(true);
  const router = useRouter();
  const searchParams = useSearchParams();
  const subscription_tier = searchParams.get("subscription_tier");
  const {
    store: {
      auth: { isAuthenticated },
    },
  } = useContext(GlobalContext);
  const validTier = Object.values(SubscriptionTier).includes(
    subscription_tier as SubscriptionTier,
  );

  const { call, loading, res } = useCallApi(
    {
      endpoint: Endpoint.SubscribeStart,
      body: null,
      query: {
        tier: subscription_tier as SubscriptionTier,
      },
      path: null,
    },
    {
      onSuccess: (res) => {
        if (res.data?.url) router.push(res.data.url);
      },
    },
  );

  useEffect(() => {
    const timeout = setTimeout(() => {
      if (isAuthenticated) {
        setDisabled(false);
        call();
      } else {
        return redirect(
          `/auth?redirect_uri=/subscribe?subscription_tier=${subscription_tier}`,
        );
      }
    }, 3000);

    return () => clearTimeout(timeout);
  }, []);

  if (!validTier) {
    return <Alert color="failure">Invalid Tier Selection</Alert>;
  }

  if (res && !res?.success) {
    return <Alert color="warning">Something went wrong...</Alert>;
  }

  return (
    <Button disabled={disabled} isProcessing={loading}>
      {disabled ? "Redirecting..." : "Proceed to Checkout"}
    </Button>
  );
};
