"use client";
import { Typography } from "@/shared/typography";
import { Button, Card } from "flowbite-react";
import { MdSchool } from "react-icons/md";
import { useHandleMessage } from "..";

export const LearnAboutBasel = () => {
  const { handleMessage } = useHandleMessage();

  return (
    <Card className="w-full">
      <Typography.Heading className="flex text-lg">
        <MdSchool className="mr-2 text-2xl" /> Learn about Basel
      </Typography.Heading>
      <Typography.Paragraph>
        Ask Basel to learn how she can help guide your career.
      </Typography.Paragraph>
      <div className="flex flex-wrap space-y-4 md:space-x-4 md:space-y-0">
        <Button
          className="w-full md:w-auto"
          gradientDuoTone="greenToBlue"
          outline
          onClick={() => handleMessage("interviews")}
        >
          Automated Interviews
        </Button>
        <Button
          className="w-full md:w-auto"
          gradientDuoTone="greenToBlue"
          outline
          onClick={() => handleMessage("bot")}
        >
          Personalized Bot
        </Button>
        <Button
          className="w-full md:w-auto"
          gradientDuoTone="greenToBlue"
          outline
          onClick={() => handleMessage("search")}
        >
          Job Search
        </Button>
        <Button
          className="w-full md:w-auto"
          gradientDuoTone="greenToBlue"
          outline
          onClick={() => handleMessage("resume")}
        >
          Dynamic Resumes
        </Button>
      </div>
    </Card>
  );
};
