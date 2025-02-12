import { FC } from "react";
import { Typography } from "@/shared/typography";
import { Card, HR } from "flowbite-react";
import { Endpoint, callApi } from "@/api";
import { Interview } from "@/types";

export const QuestionsList: FC<{ interview_uuid: Interview["uuid"] }> = async ({
  interview_uuid,
}) => {
  const interviewQuestionsRes = await callApi({
    endpoint: Endpoint.GetInterviewQuestions,
    body: null,
    path: null,
    query: { interview_uuid: interview_uuid },
  });
  const interviewQuestions = interviewQuestionsRes.data;
  if (!interviewQuestions) return null;

  if (!interviewQuestions.length) {
    return (
      <Card>
        <Typography.Heading className="text-xl">
          Nothing Found!
        </Typography.Heading>
        <Typography.Paragraph>
          There are no questions attached to this interview.
        </Typography.Paragraph>
      </Card>
    );
  }

  return (
    <Card>
      <Typography.Heading className="text-3xl">Questions</Typography.Heading>
      <ol>
        {interviewQuestions.map((q, i) => (
          <li key={q.uuid}>
            <div className="flex items-end gap-2">
              <Typography.Heading className="text-xl">
                {i + 1}.
              </Typography.Heading>
              <Typography.Paragraph>{q.question}</Typography.Paragraph>
            </div>
            <HR />
          </li>
        ))}
      </ol>
    </Card>
  );
};
