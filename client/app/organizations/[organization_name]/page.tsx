import { PageHeader } from "@/shared/layout/page-header";
import { Typography } from "@/shared/typography";
import Image from "next/image";
import { PiUsersBold } from "react-icons/pi";
import { AddOrganizationInterviewButton, Members } from "./components";
import { Breadcrumb, BreadcrumbItem, Card, HR } from "flowbite-react";
import { Endpoint, callApi } from "@/api";
import { GrOrganization } from "react-icons/gr";
import { InterviewsList } from "@/shared/interviews-list";

export default async function Page(props: {
  params: Promise<{ organization_name: string }>;
}) {
  const params = await props.params;
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
      <Breadcrumb>
        <BreadcrumbItem icon={GrOrganization} href="/organizations">
          My Organizations
        </BreadcrumbItem>
      </Breadcrumb>
      <Card>
        <div className="flex flex-col gap-4 md:flex-row">
          <div className="flex w-full items-center justify-center p-4 md:w-1/3">
            {organization.logo ? (
              <Image
                src={organization.logo?.url || ""}
                alt="organization logo"
                width={300}
                height={200}
                className="h-[200px] w-full rounded object-contain"
              />
            ) : (
              <GrOrganization className="size-32 text-slate-400 dark:text-slate-700" />
            )}
          </div>
          <div className="flex flex-row space-y-2 md:w-2/3 md:flex-col">
            <PageHeader title={organization.name} />
            <Typography.Heading className="flex items-center gap-2">
              <PiUsersBold className="size-4" />
              {organization.users.length === 1
                ? "1 Member"
                : `${organization.users.length} Members`}
            </Typography.Heading>
            <Typography.Paragraph>
              {organization.description}
            </Typography.Paragraph>
          </div>
        </div>
      </Card>
      <HR />
      <div className="flex flex-col gap-2 md:flex-row">
        <div className="w-full md:w-1/3">
          <Members users={organization.users} />
        </div>
        <div className="w-full md:w-2/3">
          <Card className="flex w-full flex-col space-y-4">
            <div className="flex justify-between">
              <Typography.Heading className="text-xl">
                Interviews
              </Typography.Heading>
              <AddOrganizationInterviewButton
                organization_uuid={organization.uuid}
                members={organization.users}
              />
            </div>
            <InterviewsList organization_uuid={organization.uuid} />
          </Card>
        </div>
      </div>
    </section>
  );
}
