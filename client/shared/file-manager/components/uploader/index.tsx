"use client";

import { Button, Card, FileInput, Label, Modal, Table } from "flowbite-react";
import { useContext } from "react";
import { GrCloudUpload } from "react-icons/gr";
import { FileManagerContext } from "../../context";

export const Uploader = () => {
  const { handleUpload, handleSetUploads, uploads, uploading } =
    useContext(FileManagerContext);

  return (
    <Modal.Body className="h-96">
      {uploads?.length ? (
        <Table className="mb-2">
          <Table.Head>
            <Table.HeadCell>File</Table.HeadCell>
            <Table.HeadCell>Size</Table.HeadCell>
          </Table.Head>
          <Table.Body>
            {Array.from(uploads).map((f, i) => (
              <Table.Row
                className="bg-white dark:border-gray-700 dark:bg-gray-800"
                key={i}
              >
                <Table.Cell>{f.name}</Table.Cell>
                <Table.Cell>{(f.size / 1048576).toFixed(2)} MB</Table.Cell>
              </Table.Row>
            ))}
          </Table.Body>
        </Table>
      ) : (
        <div className="flex w-full items-center justify-center">
          <Label
            htmlFor="dropzone-file"
            className="flex h-64 w-full cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed border-gray-300 bg-gray-50 hover:bg-gray-100 dark:border-gray-600 dark:bg-gray-700 dark:hover:border-gray-500 dark:hover:bg-gray-600"
          >
            <div className="flex flex-col items-center justify-center pb-6 pt-5">
              <GrCloudUpload className="mb-4 h-8 w-8 text-gray-500 dark:text-gray-400" />
              <p className="mb-2 text-sm text-gray-500 dark:text-gray-400">
                <span className="font-semibold">Click to upload</span> or drag
                and drop
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400">
                PDF, PNG, or JPG (MAX. 10mb)
              </p>
            </div>
            <FileInput
              id="dropzone-file"
              className="hidden"
              onChange={(e) => handleSetUploads(e.target.files)}
              multiple
            />
          </Label>
        </div>
      )}
    </Modal.Body>
  );
};
