"use client";

import { Button, Table } from "flowbite-react";
import dayjs from "dayjs";
import { LuDownload } from "react-icons/lu";
import { useContext } from "react";
import { FileManagerContext } from "@/shared/file-manager/context";
import clsx from "clsx";

export const FilesListTable = () => {
  const {
    files,
    handleSelectFile,
    selectedFiles,
    handleDownloadFile,
    downloading,
    handleSelect,
  } = useContext(FileManagerContext);

  return (
    <Table hoverable>
      <Table.Head>
        <Table.HeadCell>File Name</Table.HeadCell>
        <Table.HeadCell className="hidden md:table-cell">
          Created At
        </Table.HeadCell>
        <Table.HeadCell className="text-center">Download</Table.HeadCell>
      </Table.Head>
      <Table.Body>
        {files.map((f) => (
          <Table.Row
            key={f.uuid}
            className={clsx({
              "cursor-pointer": !!handleSelect,
              "bg-green-100 bg-green-200 hover:bg-green-100 hover:dark:bg-green-50":
                selectedFiles.findIndex((sf) => sf.uuid === f.uuid) > -1,
            })}
            onClick={() => !!handleSelect && handleSelectFile(f)}
          >
            <Table.Cell>{f.file_name}</Table.Cell>
            <Table.Cell className="hidden md:table-cell">
              {dayjs.utc(f.created_at).local().format("MMM D YYYY h:mma")}
            </Table.Cell>
            <Table.Cell
              className="flex justify-center text-center"
              onClick={(e) => e.stopPropagation()}
            >
              <Button
                outline
                color="purple"
                isProcessing={downloading === f.uuid}
                onClick={() => {
                  handleDownloadFile(f);
                }}
              >
                <LuDownload className="h-4 w-4" />
              </Button>
            </Table.Cell>
          </Table.Row>
        ))}
      </Table.Body>
    </Table>
  );
};
