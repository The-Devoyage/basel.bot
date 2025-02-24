import { Endpoint, callApi } from "@/api";
import { Typography } from "@/shared/typography";
import { Interview } from "@/types";
import { Card } from "flowbite-react";
import { AssessmentsTable } from "./components";

const Page = async (props: {
  params: Promise<{ interview_uuid: Interview["uuid"] }>;
}) => {
  const params = await props.params;
  //TODO: Add pagination
  const interviewAssessmentsRes = await callApi({
    endpoint: Endpoint.GetInterviewAssessments,
    query: { interview_uuid: params.interview_uuid },
    body: null,
    path: null,
  });
  const interviewAssessments = interviewAssessmentsRes.data || [];

  return (
    <Card className="w-full overflow-x-auto">
      <Typography.Heading className="text-2xl">Candidates</Typography.Heading>
      {interviewAssessments.length ? (
        <AssessmentsTable interviewAssessments={interviewAssessments} />
      ) : (
        <div className="flex flex-col items-center justify-center rounded border p-4">
          <Typography.Heading className="text-xl">
            Nothing Found!
          </Typography.Heading>
          <Typography.Paragraph>
            No candidates have taken this interview.
          </Typography.Paragraph>
        </div>
      )}
    </Card>
  );
};

export default Page;
