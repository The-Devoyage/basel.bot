import { PageHeader } from "@/shared/layout/page-header";
import { Typography } from "@/shared/typography";
import Image from "next/image";
import { HR } from "flowbite-react";
import { TfiWrite } from "react-icons/tfi";

export default function Page({
  params,
}: {
  params: { interveiw_uuid: string };
}) {
  const interview = { name: "Nick Co" };
  // const interviewRes = callApi({endpoint: Endpoint.GetInterview})

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
          <PageHeader title={interview.name} />
          <Typography.Heading className="flex items-center gap-2">
            <TfiWrite className="h-4 w-4" />
            200 responses
          </Typography.Heading>
        </div>
      </div>
      <HR />
    </section>
  );
}
