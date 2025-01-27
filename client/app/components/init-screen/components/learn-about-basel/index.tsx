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
        Discover how Basel can help guide careers with powerful tools, designed
        to make job searching smarter and more impactful.
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
          onClick={() => handleMessage("describe_standup")}
        >
          Standups
        </Button>
        <Button
          className="w-full md:w-auto"
          gradientDuoTone="greenToBlue"
          outline
          onClick={() => handleMessage("shareable_links")}
        >
          Shareable Links
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
