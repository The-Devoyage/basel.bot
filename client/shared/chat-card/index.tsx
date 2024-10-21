import { Card } from "flowbite-react";
import { BiSolidLeaf } from "react-icons/bi";
import { forwardRef } from "react";
import { Typography } from "../typography";
import { Message } from "@/types";
import { PiUserCircleDuotone } from "react-icons/pi";
import Markdown from "react-markdown";
import "./module.styles.css";

interface ChatCardProps {
  message: Message;
}

export const ChatCard = forwardRef<HTMLDivElement, ChatCardProps>(
  ({ message }, ref) => {
    const isBot = message.sender === "bot";
    const getIcon = () => {
      switch (message.sender) {
        case "bot":
          return <BiSolidLeaf className="h-6 w-6 text-green-400" />;
        default:
          return <PiUserCircleDuotone className="h-8 w-8 text-blue-400" />;
      }
    };

    return (
      <div ref={ref}>
        <Card
          style={{
            borderLeft: isBot ? "4px solid #34D399" : "4px solid #3B82F6",
          }}
        >
          <div className="flex flex-row items-center space-x-2">
            {getIcon()}
            <Typography.Heading className="text-xl capitalize">
              {isBot ? "Basel" : "You"}
            </Typography.Heading>
          </div>
          <Markdown className="prose w-full break-words dark:text-slate-300">
            {message.text}
          </Markdown>
        </Card>
      </div>
    );
  },
);
