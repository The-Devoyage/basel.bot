import { Interview } from "@/types";
import clsx from "clsx";
import { Tooltip } from "flowbite-react";
import { FC } from "react";
import { TbCircleCheck, TbCircleDashed, TbProgress } from "react-icons/tb";

export const StatusBadge: FC<{ interview: Interview }> = ({ interview }) => {
  const started = interview.started;
  const submitted = interview.submitted;

  const getBadge = () => {
    const className = "ml-2 h-8 w-8";
    if (submitted) {
      return <TbCircleCheck className={clsx(className, "text-green-400")} />;
    }
    if (started) {
      return (
        <TbProgress
          className={clsx(className, "text-blue-600", "dark:text-blue-500")}
        />
      );
    }
    return (
      <TbCircleDashed
        className={clsx(className, "text-slate-300", "dark:text-slate-600")}
      />
    );
  };

  const getContent = () => {
    if (submitted) {
      return "Interview Submitted - Editing is now disabled.";
    }
    if (started) {
      return "In Progress - Finish answering questions to continue.";
    }
    return "Not started - Take this interview today!";
  };

  return <Tooltip content={getContent()}>{getBadge()}</Tooltip>;
};
