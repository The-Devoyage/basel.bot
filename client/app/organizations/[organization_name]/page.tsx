import { PageHeader } from "@/shared/layout/page-header";
import { Typography } from "@/shared/typography";
import Image from "next/image";
import { PiUsersBold } from "react-icons/pi";
import { Members } from "./components";
import { Card, HR } from "flowbite-react";
import { InterviewsList } from "@/app/interviews/components";

export default function Page({
  params,
}: {
  params: { organization_name: string };
}) {
  const organization = { name: "Nick Co" };

  return (
    <section className="container mx-auto flex w-full flex-col space-y-4 p-4">
      <div className="flex gap-4">
        <Image
          src="https://placehold.co/600x400/png"
          alt="organization logo"
          width={250}
          height={250}
          className="rounded object-cover"
        />
        <div className="flex flex-col space-y-2">
          <PageHeader title={organization.name} />
          <Typography.Heading className="flex items-center gap-2">
            <PiUsersBold className="h-4 w-4" />1 Member
          </Typography.Heading>
        </div>
      </div>
      <HR />
      <div className="flex gap-2">
        <div className="w-1/3">
          <Members />
        </div>
        <Card className="flex w-full flex-col space-y-4">
          <Typography.Heading className="text-xl">
            Interviews
          </Typography.Heading>
          <InterviewsList />
        </Card>
      </div>
    </section>
  );
}
