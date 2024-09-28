import { Card } from "flowbite-react";
import { BiSolidLeaf } from "react-icons/bi";
import { FC } from "react";
import { Typography } from "../typography";
import { Message } from "@/types";
import { PiUserCircleDuotone } from "react-icons/pi";

interface ChatCardProps {
  message: Message;
}

export const ChatCard: FC<ChatCardProps> = ({ message }) => {
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
      <Typography.Paragraph>{message.text}</Typography.Paragraph>
    </Card>
  );
};
