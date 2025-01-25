import { PageHeader } from "@/shared/layout/page-header";
import { Alert } from "flowbite-react";
import { InterviewsList } from "./components";
import { AddInterviewButton } from "@/shared/add-interview-button";

const InterviewsPage = async () => (
  <section className="flex w-full flex-col space-y-4">
    <div className="flex items-center justify-between">
      <PageHeader title="Interviews" />
      <AddInterviewButton />
    </div>
    <Alert color="purple">
      <h2 className="text-xl">Straight to the Chase</h2>
      <p>
        Skip the application and instantly interview for any job with Basel.
      </p>
    </Alert>
    <InterviewsList />
  </section>
);

export default InterviewsPage;
