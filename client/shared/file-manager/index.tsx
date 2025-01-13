"use client";

import { Button, Modal, Tabs } from "flowbite-react";
import { FC } from "react";
import { FaFolderOpen } from "react-icons/fa";
import { FileList, Uploader } from "./components";
import { GrCloudUpload } from "react-icons/gr";
import { FileManagerContextProvider } from "./context";

export const FileManager: FC<{ show: boolean; onClose: () => void }> = ({
  show,
  onClose,
}) => (
  <FileManagerContextProvider>
    <Modal show={show} size="5xl" onClose={onClose}>
      <Modal.Header>File Manager</Modal.Header>
      <Tabs variant="fullWidth">
        <Tabs.Item title="My Files" icon={FaFolderOpen}>
          <FileList />
        </Tabs.Item>
        <Tabs.Item title="Upload" icon={GrCloudUpload}>
          <Uploader />
        </Tabs.Item>
      </Tabs>
      <Modal.Footer className="flex items-center justify-end">
        <Button outline color="green">
          Select
        </Button>
      </Modal.Footer>
    </Modal>
  </FileManagerContextProvider>
);
