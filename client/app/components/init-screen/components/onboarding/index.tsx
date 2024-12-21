import { Endpoint, callApi } from "@/api";
import { Typography } from "@/shared/typography";
import { Card, Progress } from "flowbite-react";
import Link from "next/link";
import { ReactNode } from "react";

export const Onboarding = async () => {
  const onboarding = await callApi({
    endpoint: Endpoint.GetOnboarding,
    query: null,
    path: null,
    body: null,
  });

  const progress = Object.values(onboarding.data || {}).reduce((prev, next) => {
    if (next) {
      prev = prev + 25;
    }
    return prev;
  }, 0);

  let msg: ReactNode = "";
  if (!onboarding.data?.metas) {
    msg = "Try chatting with Basel to get started!";
  } else if (!onboarding.data?.interviews) {
    msg = "Try taking an interview to continue onboarding.";
  } else if (!onboarding?.data?.links) {
    msg = (
      <span>
        Try creating a{" "}
        <Link href="/my-basel" className="underline">
          shareable link
        </Link>{" "}
        to share your profile.
      </span>
    );
  } else if (!onboarding?.data?.views) {
    msg = "Try sharing your link to accumulate views.";
  }

  if (Object.values(onboarding?.data || {}).every((v) => !!v)) {
    return null;
  }

  return (
    <Card className="w-full">
      <Typography.Heading className="text-lg">
        Getting Started
      </Typography.Heading>
      <Progress progress={progress} color="green" />
      <Typography.Paragraph>Welcome to Basel! {msg}</Typography.Paragraph>
    </Card>
  );
};
