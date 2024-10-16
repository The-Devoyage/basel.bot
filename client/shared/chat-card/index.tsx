import { Card } from "flowbite-react";
import { BiSolidLeaf } from "react-icons/bi";
import { forwardRef } from "react";
import { Typography } from "../typography";
import { Message } from "@/types";
import { PiUserCircleDuotone } from "react-icons/pi";
import Image from "next/image";

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
          <Typography.Paragraph className="break-words">
            {message.text}
          </Typography.Paragraph>
        </Card>
        <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4">
          {message.products?.map((product) => (
            <Card
              key={product.name}
              renderImage={() => (
                <div className="flex cursor-pointer justify-center p-4">
                  <Image
                    width={200}
                    height={300}
                    src={product.thumbnail_url}
                    alt={product.description}
                  />
                </div>
              )}
              theme={{
                root: {
                  base: "flex rounded-lg border border-gray-200 bg-white shadow-md ring-green-400 ring-opacity-50 hover:ring-2 dark:border-gray-700 dark:bg-gray-800",
                  children: `flex h-full cursor-pointer flex-col justify-start gap-4 p-6 transition-shadow duration-300 ease-in-out hover:shadow-xl`,
                },
              }}
              onClick={() => window.open(product.url, "_blank")}
            >
              <Typography.Heading>{product.name}</Typography.Heading>
              <Typography.Paragraph>{product.description}</Typography.Paragraph>
            </Card>
          ))}
        </div>
      </div>
    );
  },
);
