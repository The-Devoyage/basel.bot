import { PageHeader } from "@/shared/layout/page-header";
import { Typography } from "@/shared/typography";
import Image from "next/image";
import { Badge, Card, HR } from "flowbite-react";
import { Endpoint, callApi } from "@/api";
import { GrOrganization } from "react-icons/gr";
import { TakeInterviewButton } from "@/app/components/init-screen/components/recent-interviews/components";
import { TfiWrite } from "react-icons/tfi";
import { toDate } from "@/utils";
import { WiTime9 } from "react-icons/wi";
import { Interview } from "@/types";
import { QuestionsList } from "./components";

export default async function Page({
  params,
}: {
  params: { interview_uuid: Interview["uuid"] };
}) {
  const interviewRes = await callApi({
    endpoint: Endpoint.GetInterview,
    body: null,
    path: null,
    query: { uuid: params.interview_uuid },
  });
  const interview = interviewRes.data;
  if (!interview) return null;

  return (
    <section className="container mx-auto flex w-full flex-col space-y-4 p-4">
      <Card>
        <div className="flex gap-4">
          <div className="flex w-1/3 items-center justify-center p-4">
            {interview.organization?.logo ? (
              <Image
                src={interview.organization.logo?.url || ""}
                alt="organization logo"
                width={300}
                height={200}
                className="h-[200px] w-full rounded object-contain"
              />
            ) : (
              <GrOrganization className="h-32 w-32 text-slate-400 dark:text-slate-700" />
            )}
          </div>
          <div className="flex w-2/3 flex-col justify-between space-y-4">
            <div className="space-y-2">
              <PageHeader title={interview.position} />
              <div className="flex gap-2">
                <Badge color="purple">
                  <div className="flex gap-2">
                    <TfiWrite className="h-4 w-4" />
                    {interview.response_count} Responses
                  </div>
                </Badge>
                <Badge color="blue">
                  <div className="flex gap-2">
                    <WiTime9 className="h-4 w-4" />
                    {toDate(interview.created_at, false)}
                  </div>
                </Badge>
              </div>
              <Typography.Paragraph>
                {interview.description}
              </Typography.Paragraph>
            </div>
            <div className="flex justify-end">
              <TakeInterviewButton interview={interview}>
                Take Interview
              </TakeInterviewButton>
            </div>
          </div>
        </div>
      </Card>
      <HR />
      <QuestionsList interview_uuid={params.interview_uuid} />
    </section>
  );
}
