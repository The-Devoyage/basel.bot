import { Endpoint, callApi } from "@/api";
import { Typography } from "@/shared/typography";
import { Alert, Card } from "flowbite-react";
import { FaCircleCheck } from "react-icons/fa6";
import { TbReportAnalytics } from "react-icons/tb";
import { TakeInterviewButton } from "./components";

export const RecentInterviews = async () => {
  const interviews = await callApi({
    endpoint: Endpoint.GetInterviews,
    query: { limit: 3 },
    body: null,
    path: null,
  });

  return (
    <div className="w-full space-y-4 rounded-md border-2 border-purple-300 p-4">
      <div className="flex items-center">
        <Typography.Heading className="flex text-lg">
          <TbReportAnalytics className="mr-2 text-2xl" />
        </Typography.Heading>
        <Typography.Heading className="text-xl">Interviews</Typography.Heading>
      </div>
      <Alert color="purple">
        <div className="flex items-center gap-2">
          <FaCircleCheck />
          Train your bot by taking guided interviews.
        </div>
      </Alert>
      <div className="grid w-full grid-cols-1 gap-4 md:grid-cols-3">
        {(interviews.data || []).map((interview) => (
          <Card
            className="border-t-4 border-t-purple-200 dark:border-t-purple-400"
            key={interview.uuid}
          >
            <div className="flex h-48 flex-col justify-between">
              <div>
                <Typography.Heading className="font-bold">
                  {interview.name}
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
              </div>
              <div className="flex w-full justify-end">
                <TakeInterviewButton interview={interview} />
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
