import { Interview } from "@/types";
import { Tooltip } from "flowbite-react";
import { FC } from "react";
import { TbCircleCheck, TbProgress } from "react-icons/tb";

export const StatusBadge: FC<{ interview: Interview }> = ({ interview }) => {
  const complete = interview.question_count === interview.response_count;

  const getBadge = () => {
    const className = "ml-2 h-6 w-6 dark:text-white";
    if (complete) {
      return <TbCircleCheck className={className} />;
    } else {
      return <TbProgress className={className} />;
    }
  };

  const getContent = () => {
    if (complete) {
      return "Interview Completed";
    } else {
      return "In Progress";
    }
  };

  return <Tooltip content={getContent()}>{getBadge()}</Tooltip>;
};
