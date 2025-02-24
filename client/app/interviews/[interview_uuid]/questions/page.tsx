import { Typography } from "@/shared/typography";
import { Card, HR } from "flowbite-react";
import { Endpoint, callApi } from "@/api";
import { Interview } from "@/types";

export default async function Page(props: {
  params: Promise<{ interview_uuid: Interview["uuid"] }>;
}) {
  const params = await props.params;
  const interviewQuestionsRes = await callApi({
    endpoint: Endpoint.GetInterviewQuestions,
    body: null,
    path: null,
    query: { interview_uuid: params.interview_uuid },
  });
  const interviewQuestions = interviewQuestionsRes.data;
  if (!interviewQuestions) return null;

  if (!interviewQuestions.length) {
    return (
      <Card className="w-full">
        <div className="flex flex-col items-center justify-center rounded border p-4">
          <Typography.Heading className="text-xl">
            Nothing Found!
          </Typography.Heading>
          <Typography.Paragraph>
            There are no questions attached to this interview.
          </Typography.Paragraph>
        </div>
      </Card>
    );
  }

  return (
    <Card>
      <Typography.Heading className="text-3xl">Questions</Typography.Heading>
      <ol>
        {interviewQuestions.map((q, i) => (
          <li key={q.uuid}>
            <div className="flex items-start">
              <Typography.Heading>{i + 1}.</Typography.Heading>
              <Typography.Paragraph>{q.question}</Typography.Paragraph>
            </div>
            <HR />
          </li>
        ))}
      </ol>
    </Card>
  );
}
