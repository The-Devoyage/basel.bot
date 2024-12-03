"use client";

import { GlobalContext } from "@/app/provider";
import { ChatCard } from "@/shared/chat-card";
import { Typography } from "@/shared/typography";
import { Message } from "@/types";
import { Alert, Button, Card } from "flowbite-react";
import { useContext } from "react";
import { MdSchool } from "react-icons/md";
import { IoLanguage } from "react-icons/io5";
import { GiTechnoHeart } from "react-icons/gi";

export const InitScreen = () => {
  const { client, slToken } = useContext(GlobalContext);

  const handleMessage = (
    type:
      | "interviews"
      | "bot"
      | "search"
      | "resume"
      | "translations"
      | "candidate",
  ) => {
    let text = "";
    switch (type) {
      case "interviews":
        text =
          "I am interested in learning about Automated Interviews. How do these work?";
        break;
      case "bot":
        text = "Who are you, Basel? What is a Career Assistant Bot?";
        break;
      case "search":
        text = "How do you help me find jobs?";
        break;
      case "resume":
        text =
          "Dynamic Resumes? So you can help keep my resume up to date at all times?";
        break;
      case "translations":
        text =
          "Basel, tell me how you can assist in language or technical translation barriers when assisting recruiters and candidates in the job hunt process.";
        break;
      case "candidate":
        text =
          "Hey Basel! I am here to talk with you about the candidate. Let me tell you who I am first, my organization, and a little about the position I am looking to fill.";
        break;
      default:
        text = "Tell me a bit about the Basel platform.";
    }

    const message: Message = {
      text,
      timestamp: new Date(),
      sender: "user",
    };

    client?.handleSend(message);
  };
  return (
    <div className="mx-auto flex h-full flex-col items-center justify-center space-y-4">
      {slToken && (
        <Alert color="info" className="space-y-4">
          <Typography.Heading className="text-xl dark:!text-slate-800">
            Welcome! Here to learn about a candidate?
          </Typography.Heading>
          <Typography.Paragraph className="mb-2 dark:text-slate-600">
            It looks like you might be here to chat about a potential hire! Tell
            Basel about yourself, the organization you are with, and the
            position you are trying to fill.
          </Typography.Paragraph>
          <Typography.Paragraph className="dark:text-slate-600">
            Basel will help you learn about this candidate so that you may
            determine if they are a good fit or not.
          </Typography.Paragraph>
          <Button
            gradientDuoTone="purpleToBlue"
            outline
            onClick={() => handleMessage("candidate")}
            className="mt-4 w-full"
          >
            Get Started
          </Button>
        </Alert>
      )}
      <ChatCard
        message={{
          text: `Hello there! I'm Basel, your personal career assistant. I am 
                   ready to help you find jobs, prepare for interviews, and keep 
                   your dynamic resume up to date. **How can I help you today?**`,
          sender: "bot",
          timestamp: new Date(),
        }}
      />
      <Card className="w-full">
        <Typography.Heading className="flex text-lg">
          <MdSchool className="mr-2 text-2xl" /> Learn about Basel
        </Typography.Heading>
        <Typography.Paragraph>
          Ask Basel to learn how she can help guide your career.
        </Typography.Paragraph>
        <Button.Group>
          <Button
            gradientDuoTone="greenToBlue"
            outline
            onClick={() => handleMessage("interviews")}
          >
            Automated Interviews
          </Button>
          <Button
            gradientDuoTone="greenToBlue"
            outline
            onClick={() => handleMessage("bot")}
          >
            Personalized Bot
          </Button>
          <Button
            gradientDuoTone="greenToBlue"
            outline
            onClick={() => handleMessage("search")}
          >
            Job Search
          </Button>
          <Button
            gradientDuoTone="greenToBlue"
            outline
            onClick={() => handleMessage("resume")}
          >
            Dynamic Resumes
          </Button>
        </Button.Group>
      </Card>
      <div className="flex flex-col p-12 md:flex-row md:space-x-8">
        <div>
          <Typography.Heading className="text-4xl">
            Break Barriers, Build Opportunities
          </Typography.Heading>
          <Typography.Paragraph className="my-4">
            Career potential shouldn’t be limited by language or technical
            knowledge gaps. Our AI-powered career assistant helps candidates and
            recruiters communicate strengths and needs clearly and confidently,
            no matter your background.
          </Typography.Paragraph>
        </div>
        <div className="flex flex-col justify-between">
          <ul className="space-y-6">
            <li className="flex gap-2">
              <div className="mr-2 flex h-12 w-12 min-w-12 items-center justify-center rounded bg-blue-800">
                <IoLanguage className="text-2xl text-blue-200" />
              </div>
              <div>
                <Typography.Heading className="text-lg">
                  Overcome Language Barriers
                </Typography.Heading>
                <Typography.Paragraph>
                  Basel specializes in translating your unique skills and
                  experiences into professional, recruiter-friendly language,
                  ensuring they are clearly and effectively communicated—no
                  matter what language you speak or where you are from.
                </Typography.Paragraph>
              </div>
            </li>
            <li className="flex gap-2">
              <div className="mr-2 flex h-12 w-12 min-w-12 items-center justify-center rounded bg-green-800">
                <GiTechnoHeart className="pt-1 text-3xl text-green-200" />
              </div>
              <div>
                <Typography.Heading className="text-lg">
                  Bridge Technical Knowledge Gaps
                </Typography.Heading>
                <Typography.Paragraph>
                  Recruiters don’t need to be technical experts to understand
                  your value—Basel bridges the gap. Basel translates your
                  technical expertise and challenges into clear,
                  recruiter-friendly language, ensuring your skills are
                  accurately represented and easy to understand for hiring
                  professionals, regardless of their technical background.
                </Typography.Paragraph>
              </div>
            </li>
          </ul>
          <Button
            gradientDuoTone="greenToBlue"
            className="mt-4 w-full"
            onClick={() => handleMessage("translations")}
          >
            Start Chatting
          </Button>
        </div>
      </div>
    </div>
  );
};
