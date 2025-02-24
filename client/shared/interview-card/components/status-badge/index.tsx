import { Interview } from "@/types";
import clsx from "clsx";
import { Tooltip } from "flowbite-react";
import { FC } from "react";
import {
  TbCircleCheck,
  TbCircleDashed,
  TbProgress,
  TbProgressCheck,
} from "react-icons/tb";

export const StatusBadge: FC<{ interview: Interview }> = ({ interview }) => {
  const complete = interview.question_count === interview.response_count;
  const started = interview.response_count > 0;
  const submitted = interview.submitted;

  const getBadge = () => {
    const className = "ml-2 h-8 w-8";
    if (submitted) {
      return <TbCircleCheck className={clsx(className, "text-green-400")} />;
    }
    if (!started)
      return (
        <TbCircleDashed
          className={clsx(className, "text-slate-300", "dark:text-slate-600")}
        />
      );
    if (complete) {
      return <TbProgressCheck className={clsx(className, "text-green-400")} />;
    } else {
      return (
        <TbProgress
          className={clsx(className, "text-blue-600", "dark:text-blue-500")}
        />
      );
    }
  };

  const getContent = () => {
    if (submitted) return "Interview Submitted - Editing is now disabled.";
    if (!started) return "Not started - Take this interview today!";
    if (complete) {
      return "All Questions Answered - Edit or submit when ready.";
    } else {
      return "In Progress - Finish answering questions to continue.";
    }
  };

  return <Tooltip content={getContent()}>{getBadge()}</Tooltip>;
};
