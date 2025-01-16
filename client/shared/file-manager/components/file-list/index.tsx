"use client";

import { useContext } from "react";
import { FileManagerContext } from "../../context";
import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";
import { EmptyFiles, FilesListTable } from "./components";

dayjs.extend(utc);

export const FileList = () => {
  const { files } = useContext(FileManagerContext);

  return (
    <div className="relative flex flex-col">
      <div className="flex-grow overflow-y-auto">
        {!files.length ? <EmptyFiles /> : <FilesListTable />}
      </div>
    </div>
  );
};
