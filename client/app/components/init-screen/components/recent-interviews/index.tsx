import { Endpoint, callApi } from "@/api";
import { Typography } from "@/shared/typography";
import { Alert, Badge, Card, Tooltip } from "flowbite-react";
import { FaCircleCheck } from "react-icons/fa6";
import { TbReportAnalytics } from "react-icons/tb";
import { TakeInterviewButton } from "./components";

export const RecentInterviews = async () => {
  const interviews = await callApi({
    endpoint: Endpoint.GetInterviews,
    query: { limit: 6 },
    body: null,
    path: null,
  });

  return (
    <div className="w-full space-y-4 rounded-md border-2 border-purple-300 bg-purple-50 p-4 dark:bg-slate-900">
      <div className="flex items-center">
        <Typography.Heading className="flex text-lg">
          <TbReportAnalytics className="mr-2 text-2xl" />
        </Typography.Heading>
        <Typography.Heading className="text-xl">Interviews</Typography.Heading>
      </div>
      <Alert color="purple">
        <div className="flex items-center gap-2">
          <FaCircleCheck />
          Train your bot with interviews generated from real postings.
        </div>
      </Alert>
      <div className="grid w-full grid-cols-1 gap-4 md:grid-cols-3">
        {(interviews.data || []).map((interview) => (
          <Card
            className="border-t-4 border-t-purple-200 dark:border-t-purple-400"
            key={interview.uuid}
          >
            <div className="h-54 flex h-full flex-col justify-between">
              <div className="flex w-full items-start justify-between">
                <Typography.Heading className="text-xl font-bold">
                  {interview.position || interview.name}
                </Typography.Heading>
              </div>
              <Typography.Heading className="italic">
                {interview.position && interview.name}
              </Typography.Heading>
              <Typography.Paragraph
                className="h-full overflow-hidden"
                style={{
                  display: "-webkit-box",
                  WebkitBoxOrient: "vertical",
                  WebkitLineClamp: 5,
                  lineHeight: "1.5",
                  maxHeight: "calc(1.5em * 5)",
                }}
              >
                {interview.description}
              </Typography.Paragraph>
              <div className="flex w-full items-end justify-between">
                <Badge color="green">{interview.organization_name}</Badge>
                <Tooltip content="Learn More">
                  <TakeInterviewButton interview={interview} />
                </Tooltip>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
