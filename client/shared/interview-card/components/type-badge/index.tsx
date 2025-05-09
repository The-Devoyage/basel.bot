import { InterviewType } from "@/types";
import { Tooltip } from "flowbite-react";
import { FC } from "react";
import { GiGraduateCap } from "react-icons/gi";
import { IoDocumentText } from "react-icons/io5";

export const InterviewTypeBadge: FC<{ interview_type: InterviewType }> = ({
  interview_type,
}) => {
  if (interview_type === InterviewType.GENERAL) {
    return (
      <Tooltip content="Mock interview generated by peer.">
        <div className="flex gap-2 py-1">
          <GiGraduateCap className="size-6 text-blue-400" />
        </div>
      </Tooltip>
    );
  }
  return (
    <Tooltip content="Official interview created by organization">
      <div className="flex gap-2 py-1">
        <IoDocumentText className="size-6 text-blue-400" />
      </div>
    </Tooltip>
  );
};
