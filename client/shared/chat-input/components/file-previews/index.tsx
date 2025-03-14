"use client";

import { Typography } from "@/shared/typography";
import { Button } from "flowbite-react";
import { useContext } from "react";
import { BiFile } from "react-icons/bi";
import { FaX } from "react-icons/fa6";
import { ChatInputContext } from "../../context";

export const FilePreviews = () => {
  const { files, setFiles } = useContext(ChatInputContext);

  if (!files.length) return null;

  return (
    <div className="flex">
      {files.map((f) => (
        <div key={f.uuid} className="rounded border-2 border-slate-600 p-1">
          <div className="flex items-center gap-2">
            <BiFile className="h-6 w-6 dark:text-white" />
            <Typography.Heading>{f.file_name}</Typography.Heading>
            <Button
              size="xs"
              outline
              color="dark"
              onClick={() =>
                setFiles((curr) => [...curr.filter((cf) => cf.uuid !== f.uuid)])
              }
            >
              <FaX />
            </Button>
          </div>
        </div>
      ))}
    </div>
  );
};
