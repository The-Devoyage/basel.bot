import { Typography } from "@/shared/typography";
import { TbReportAnalytics } from "react-icons/tb";
import {
  ListInterviews,
  SearchInterviewsButton,
  InterviewsWelcome,
} from "./components";
import { InterviewContextProvider } from "./context";
import { AddInterviewButton } from "@/shared/add-interview-button";

export const RecentInterviews = () => (
  <div className="w-full space-y-4 rounded-md border-2 border-purple-300 bg-purple-50 p-4 dark:bg-slate-900">
    <div className="flex items-center">
      <Typography.Heading className="flex text-lg">
        <TbReportAnalytics className="mr-2 text-2xl" />
      </Typography.Heading>
      <div className="flex w-full items-center justify-between">
        <Typography.Heading className="text-xl">Interviews</Typography.Heading>
        <AddInterviewButton />
      </div>
    </div>
    <InterviewsWelcome />
    <InterviewContextProvider>
      <ListInterviews />
      <div className="block gap-2 space-y-2 md:flex md:space-y-0">
        <SearchInterviewsButton />
      </div>
    </InterviewContextProvider>
  </div>
);
