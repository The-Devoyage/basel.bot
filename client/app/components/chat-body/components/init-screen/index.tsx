"use client";

import { GlobalContext } from "@/app/provider";
import { ChatCard } from "@/shared/chat-card";
import { Typography } from "@/shared/typography";
import { Message } from "@/types";
import { Avatar, Button, Card } from "flowbite-react";
import { useContext } from "react";
import { MdSchool } from "react-icons/md";
import Image from "next/image";
import { IoLanguage } from "react-icons/io5";
import { GiTechnoHeart } from "react-icons/gi";

export const InitScreen = () => {
  const { client } = useContext(GlobalContext);

  const handleMessage = (type: "interviews" | "bot" | "search" | "resume") => {
    let text = "";
    switch (type) {
      case "interviews":
        text =
          "I am interested in learning about Basel's Automated Interviews. How do these work?";
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
          Ask Basel and learn how she can help guide your career.
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
      <div className="space-y-4">
        <Typography.Heading className="text-4xl">
          Break Barriers, Build Opportunities
        </Typography.Heading>
        <div className="flex space-x-4">
          <div>
            <Typography.Paragraph className="mb-4">
              At Basel, we believe that career potential shouldn’t be limited by
              language or technical knowledge gaps. Our AI-powered career
              assistant helps candidates and recruiters communicate your
              strengths and needs clearly and confidently, no matter your
              background.
            </Typography.Paragraph>
            <ul className="space-y-4">
              <li className="space-y-4">
                <div className="flex items-center">
                  <div className="mr-2 flex h-12 w-12 items-center justify-center rounded-full bg-blue-800 shadow-xl shadow-blue-700/50">
                    <IoLanguage className="text-3xl text-blue-200" />
                  </div>
                  <Typography.Heading className="text-lg">
                    Overcome Language Barriers
                  </Typography.Heading>
                </div>
                <Typography.Paragraph>
                  Basel translates your skills and experiences into
                  professional, recruiter-friendly language.
                </Typography.Paragraph>
              </li>
              <li className="space-y-4">
                <div className="flex items-center">
                  <div className="mr-2 flex h-12 w-12 items-center justify-center rounded-full bg-green-600 shadow-xl shadow-green-700/50">
                    <GiTechnoHeart className="text-3xl text-green-200" />
                  </div>
                  <Typography.Heading className="text-lg">
                    Bridge Technical Knowledge Gaps
                  </Typography.Heading>
                </div>
                <Typography.Paragraph>
                  Don’t know the right terminology? Our intelligent guidance
                  ensures your resume and interviews reflect your expertise.
                </Typography.Paragraph>
              </li>
            </ul>
            <Button gradientDuoTone="greenToBlue" className="mt-4 w-full">
              Start Chatting
            </Button>
          </div>
          <Image
            width="870"
            height="200"
            alt="CTA Break Barriers Image"
            src="https://picsum.photos/id/870/200/300?grayscale&blur=2"
            className="rounded"
          />
        </div>
      </div>
    </div>
  );
};
