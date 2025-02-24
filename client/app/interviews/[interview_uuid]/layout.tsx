import { Breadcrumb, BreadcrumbItem, HR } from "flowbite-react";
import { Endpoint, callApi } from "@/api";
import { TfiWrite } from "react-icons/tfi";
import { Interview } from "@/types";
import { InterviewPageProvider } from "./context";
import { InterviewNav, InterviewPageHeader } from "./components";

export default async function Layout(props: {
  params: Promise<{ interview_uuid: Interview["uuid"] }>;
  children: React.ReactNode;
}) {
  const params = await props.params;
  const interviewRes = await callApi({
    endpoint: Endpoint.GetInterview,
    body: null,
    path: null,
    query: { uuid: params.interview_uuid },
  });
  const interview = interviewRes.data;

  const organizationRes = await callApi({
    endpoint: Endpoint.GetOrganizations,
    body: null,
    path: null,
    query: { my_organizations: true },
  });
  const organizations = organizationRes.data || [];

  if (!interview) return null;

  return (
    <InterviewPageProvider interview={interview} organizations={organizations}>
      <section className="container mx-auto flex w-full flex-col space-y-4 p-4">
        <Breadcrumb>
          <BreadcrumbItem icon={TfiWrite} href="/interviews">
            Interviews
          </BreadcrumbItem>
        </Breadcrumb>
        <InterviewPageHeader />
        <HR />
        <div className="flex flex-col items-start gap-2 md:flex-row">
          <InterviewNav />
          {props.children}
        </div>
      </section>
    </InterviewPageProvider>
  );
}
