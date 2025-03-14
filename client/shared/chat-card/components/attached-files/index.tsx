import { FC } from "react";
import { SocketMessage } from "@/types";
import { BiFile } from "react-icons/bi";
import { Typography } from "@/shared/typography";

export const AttachedFiles: FC<{ message: SocketMessage }> = ({ message }) => {
  if (!message.files?.length) return null;
  return (
    <div className="flex">
      {message.files?.map((f) => (
        <div key={f.uuid} className="rounded border-2 border-slate-600 p-1">
          <div className="flex items-center gap-2">
            <BiFile className="h-6 w-6 dark:text-white" />
            <Typography.Heading>{f.file_name}</Typography.Heading>
          </div>
        </div>
      ))}
    </div>
  );
};
