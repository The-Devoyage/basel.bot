import { PageHeader } from "@/shared/layout/page-header";
import { Typography } from "@/shared/typography";
import Image from "next/image";
import { PiUsersBold } from "react-icons/pi";
import { Members } from "./components";
import { Card, HR } from "flowbite-react";
import { InterviewsList } from "@/app/interviews/components";
import { Endpoint, callApi } from "@/api";

export default async function Page({
  params,
}: {
  params: { organization_name: string };
}) {
  const organizationRes = await callApi({
    endpoint: Endpoint.GetOrganization,
    query: { slug: params.organization_name },
    body: null,
    path: null,
  });
  const organization = organizationRes.data;

  if (!organization) return null;

  return (
    <section className="container mx-auto flex w-full flex-col space-y-4 p-4">
      <div className="flex gap-4">
        <div className="mt-8 w-1/3">
          <Image
            src={organization.logo?.url || "https://placehold.co/600x400/png"}
            alt="organization logo"
            width={300}
            height={200}
            className="h-[200px] w-full rounded object-contain"
          />
        </div>
        <div className="flex w-2/3 flex-col space-y-2">
          <PageHeader title={organization.name} />
          <Typography.Heading className="flex items-center gap-2">
            <PiUsersBold className="h-4 w-4" />
            {organization.users.length === 1
              ? "1 Member"
              : `${organization.users.length} Members`}
          </Typography.Heading>
          <Typography.Paragraph>
            {organization.description}
          </Typography.Paragraph>
        </div>
      </div>
      <HR />
      <div className="flex gap-2">
        <div className="w-1/3">
          <Members users={organization.users} />
        </div>
        <div className="w-2/3">
          <Card className="flex w-full flex-col space-y-4">
            <Typography.Heading className="text-xl">
              Interviews
            </Typography.Heading>
            <InterviewsList />
          </Card>
        </div>
      </div>
    </section>
  );
}
