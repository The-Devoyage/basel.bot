"use client";

import { PageHeader } from "@/shared/layout/page-header";
import Image from "next/image";
import { Badge, Card } from "flowbite-react";
import { GrOrganization } from "react-icons/gr";
import { TakeInterviewButton } from "@/app/components/init-screen/components/recent-interviews/components";
import { TfiWrite } from "react-icons/tfi";
import { toDate } from "@/utils";
import { WiTime9 } from "react-icons/wi";
import Link from "next/link";
import { useContext } from "react";
import { InterviewPageContext } from "../../context";

export const InterviewPageHeader = () => {
  const { interview } = useContext(InterviewPageContext);

  if (!interview) return null;

  return (
    <Card>
      <div className="flex flex-col gap-4 md:flex-row">
        <div className="flex w-full items-center justify-center p-4 md:w-1/3">
          {interview.organization?.logo ? (
            <Image
              src={interview.organization.logo?.url || ""}
              alt="organization logo"
              width={300}
              height={200}
              className="h-[200px] w-full rounded object-contain"
            />
          ) : (
            <GrOrganization className="size-32 text-slate-400 dark:text-slate-700" />
          )}
        </div>
        <div className="flex w-full flex-col justify-between space-y-4 md:w-2/3">
          <div className="space-y-2">
            <PageHeader title={interview.position} />
            <div className="flex gap-2">
              {interview.organization && (
                <Link href={`/organizations/${interview.organization.slug}`}>
                  <Badge
                    color="blue"
                    role="button"
                    className="cursor-pointer hover:ring-2 hover:ring-blue-400"
                  >
                    <div className="flex h-full gap-2 py-1">
                      <GrOrganization className="h-4 w-4 text-slate-400 dark:text-slate-700" />
                      {interview.organization!.name}
                    </div>
                  </Badge>
                </Link>
              )}
              <Badge color="purple">
                <div className="flex gap-2 py-1">
                  <TfiWrite className="size-4" />
                  {interview.total_response_count} Responses
                </div>
              </Badge>
              <Badge color="green">
                <div className="flex gap-2 py-1">
                  <WiTime9 className="size-4" />
                  {toDate(interview.created_at, false)}
                </div>
              </Badge>
            </div>
          </div>
          <div className="flex justify-end">
            <TakeInterviewButton interview={interview} action="take_interview">
              Take Interview
            </TakeInterviewButton>
          </div>
        </div>
      </div>
    </Card>
  );
};
