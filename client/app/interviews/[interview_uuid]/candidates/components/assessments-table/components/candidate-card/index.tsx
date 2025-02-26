import { Typography } from "@/shared/typography";
import { InterviewAssessment } from "@/types/interview_assessment";
import { Avatar, Button, Card, Rating, RatingStar } from "flowbite-react";
import { FC } from "react";
import { AssessmentResults } from "./components";

export const CandidateCard: FC<{ interviewAssessment: InterviewAssessment }> = ({
  interviewAssessment,
}) => {
  return (
    <Card className="border-t-4 border-t-green-400 dark:border-t-green-400">
      <div className="flex flex-col justify-center gap-4 ">
        <div className="flex flex-col items-center justify-between gap-4">
          <div className="flex flex-col items-center gap-4">
            <Avatar
              rounded
              img={interviewAssessment.user.profile_image?.url}
              placeholderInitials={interviewAssessment.user.first_initial}
              size="lg"
              bordered
              color="success"
              theme={{
                root: {
                  img: {
                    on: "flex items-center justify-center object-cover",
                    placeholder: "mt-6 text-gray-400",
                  },
                },
              }}
            />
            <Typography.Heading className="text-center text-lg">
              {interviewAssessment.user.full_name ?? "--"}
            </Typography.Heading>
            <Rating>
              {Array.from({ length: interviewAssessment.overall }, (_, i) => (
                <RatingStar key={i} />
              ))}
              {Array.from(
                { length: 5 - interviewAssessment.overall },
                (_, i) => (
                  <RatingStar key={i} filled={false} />
                ),
              )}
            </Rating>
          </div>
          <Button
            color="green"
            outline
            size="sm"
            href={`/chat?interview_assessment_uuid=${interviewAssessment.uuid}`}
          >
            Interview
          </Button>
        </div>
        <AssessmentResults interviewAssessment={interviewAssessment} />
      </div>
    </Card>
  );
};
