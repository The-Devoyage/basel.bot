import { Card } from "flowbite-react";
import { BiSolidLeaf } from "react-icons/bi";
import { forwardRef } from "react";
import { Typography } from "../typography";
import { Message } from "@/types";
import { PiUserCircleDuotone } from "react-icons/pi";
import Markdown from "react-markdown";
import "./module.styles.css";
import { FooterButtons } from "./components";

interface ChatCardProps {
  message: Message;
  icon?: React.ReactNode;
  loading?: boolean;
}

export const ChatCard = forwardRef<HTMLDivElement, ChatCardProps>(
  ({ message, icon, loading }, ref) => {
    const isBot = message.sender === "bot";
    const getIcon = () => {
      if (icon) return icon;
      switch (message.sender) {
        case "bot":
          return <BiSolidLeaf className="h-6 w-6 text-green-400" />;
        default:
          return <PiUserCircleDuotone className="h-8 w-8 text-blue-400" />;
      }
    };

    return (
      <div ref={ref} className="w-full">
        <Card
          style={{
            borderLeft: isBot ? "4px solid #34D399" : "4px solid #3B82F6",
            borderTop: "none",
            borderRight: "none",
            borderBottom: "none",
            boxShadow: isBot
              ? "-11px 3px 20px RGBA(5, 122, 85, 0.3)"
              : "-7px 3px 20px RGBA(118, 169, 250, 0.2)",
          }}
        >
          <div className="flex flex-row items-center space-x-2">
            {getIcon()}
            <Typography.Heading className="text-xl capitalize">
              {isBot ? "Basel" : "You"}
            </Typography.Heading>
          </div>
          {!loading ? (
            <Markdown className="prose w-full break-words dark:text-slate-300">
              {message.text}
            </Markdown>
          ) : (
            Array.from({ length: 1 }).map((_, index) => (
              <div key={index} className="w-full animate-pulse">
                <div className="mb-2 h-4 rounded bg-gray-200 dark:bg-slate-500" />
                <div className="mb-2 h-4 rounded bg-gray-200 dark:bg-slate-500" />
                <div className="mb-2 h-4 rounded bg-gray-200 dark:bg-slate-500" />
              </div>
            ))
          )}
          <FooterButtons buttons={message.buttons} />
        </Card>
      </div>
    );
  },
);
