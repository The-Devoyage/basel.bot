import { PageHeader } from "@/shared/layout/page-header";
import { Alert } from "flowbite-react";
import { InterviewsList } from "./components";
import { AddInterviewButton } from "@/shared/add-interview-button";

const InterviewsPage = async () => (
  <section className="container mx-auto flex w-full flex-col space-y-4 p-4">
    <div className="flex items-center justify-between">
      <PageHeader title="Interviews" />
      <AddInterviewButton />
    </div>
    <Alert color="purple" className="border-4 border-purple-500">
      <h2 className="text-xl">Start Conversations, Not Applications</h2>
      <p>
        Skip the application and jump straight to the interview. Basel is here
        to sync your profile with the application.
      </p>
    </Alert>{" "}
    <InterviewsList />
  </section>
);

export default InterviewsPage;
