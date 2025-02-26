import { InterviewAssesment } from "@/types/interview_assessment";
import { FC } from "react";
import { CandidateCard } from "./components/candidate-card";

export const AssessmentsTable: FC<{
  interviewAssessments: InterviewAssesment[];
}> = ({ interviewAssessments }) => (
  <div className="grid grid-cols-3 gap-2">
    {interviewAssessments.map((ia) => (
      <div className="col-span-3 lg:col-span-1" key={ia.uuid}>
        <CandidateCard interviewAssessment={ia} />
      </div>
    ))}
  </div>
);
