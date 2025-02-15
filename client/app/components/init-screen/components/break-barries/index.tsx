import { Typography } from "@/shared/typography";
import { GiTechnoHeart } from "react-icons/gi";
import { IoLanguage } from "react-icons/io5";
import { ChatButton } from "./components";

export const BreakBarriers = () => (
  <div className="flex flex-col rounded-md border-2 p-4 md:flex-row md:space-x-12">
    <div>
      <Typography.Heading className="text-4xl">
        Break Barriers, Build Opportunities
      </Typography.Heading>
      <Typography.Paragraph className="my-4">
        Career potential shouldn’t be limited by language or technical knowledge
        gaps. Our AI-powered career assistant helps candidates and recruiters
        communicate strengths and needs clearly and confidently, no matter your
        background.
      </Typography.Paragraph>
    </div>
    <div className="flex flex-col justify-between">
      <ul className="space-y-6">
        <li className="flex gap-2">
          <div className="mr-2 flex size-12 min-w-12 items-center justify-center rounded bg-blue-800">
            <IoLanguage className="text-2xl text-blue-200" />
          </div>
          <div className="space-y-2">
            <Typography.Heading className="text-lg">
              Overcome Language Barriers
            </Typography.Heading>
            <Typography.Paragraph>
              Basel specializes in translating your unique skills and
              experiences into professional, recruiter-friendly language,
              ensuring they are clearly and effectively communicated—no matter
              what language you speak or where you are from.
            </Typography.Paragraph>
          </div>
        </li>
        <li className="flex gap-2">
          <div className="mr-2 flex size-12 min-w-12 items-center justify-center rounded bg-green-800">
            <GiTechnoHeart className="pt-1 text-3xl text-green-200" />
          </div>
          <div className="space-y-2">
            <Typography.Heading className="text-lg">
              Bridge Technical Knowledge Gaps
            </Typography.Heading>
            <Typography.Paragraph>
              Recruiters don’t need to be technical experts to understand your
              value—Basel bridges the gap. Basel translates your technical
              expertise and challenges into clear, recruiter-friendly language,
              ensuring your skills are accurately represented and easy to
              understand for hiring professionals, regardless of their technical
              background.
            </Typography.Paragraph>
          </div>
        </li>
      </ul>
      <ChatButton />
    </div>
  </div>
);
