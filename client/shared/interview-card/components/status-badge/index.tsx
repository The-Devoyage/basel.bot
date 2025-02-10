import { Interview } from "@/types";
import clsx from "clsx";
import { Tooltip } from "flowbite-react";
import { FC } from "react";
import { TbCircleCheck, TbCircleDashed, TbProgress } from "react-icons/tb";

export const StatusBadge: FC<{ interview: Interview }> = ({ interview }) => {
  const complete = interview.question_count === interview.response_count;
  const started = interview.response_count > 0;

  const getBadge = () => {
    const className = "ml-2 h-8 w-8";
    if (!started)
      return (
        <TbCircleDashed
          className={clsx(className, "text-slate-300", "dark:text-slate-600")}
        />
      );
    if (complete) {
      return <TbCircleCheck className={clsx(className, "text-green-400")} />;
    } else {
      return (
        <TbProgress
          className={clsx(className, "text-blue-600", "dark:text-blue-500")}
        />
      );
    }
  };

  const getContent = () => {
    if (!started) return "Not Started";
    if (complete) {
      return "Interview Completed";
    } else {
      return "In Progress";
    }
  };

  return <Tooltip content={getContent()}>{getBadge()}</Tooltip>;
};
