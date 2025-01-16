"use client";

import { FC, useRef } from "react";
import { Button, Modal, Pagination, Tabs, TabsRef } from "flowbite-react";
import { FaFolderOpen } from "react-icons/fa";
import { FileList, Uploader } from "./components";
import { GrCloudUpload } from "react-icons/gr";
import { FileManagerContext, FileManagerContextProvider } from "./context";
import { File } from "@/types";

export const FileManager: FC<{
  show: boolean;
  onClose: () => void;
  multiple?: boolean;
  onSelect?: (files: File[]) => void;
}> = ({ show, onClose, multiple, onSelect }) => {
  const tabsRef = useRef<TabsRef>(null);

  return (
    <FileManagerContextProvider
      show={show}
      tabsRef={tabsRef.current}
      multiple={multiple}
      onSelect={onSelect}
    >
      <Modal show={show} size="5xl" onClose={onClose}>
        <Modal.Header>File Manager</Modal.Header>
        <FileManagerContext.Consumer>
          {({
            activeTab,
            handleTabChange,
            pagination,
            handlePageChange,
            handleSetUploads,
            uploading,
            handleUpload,
            uploads,
            selectedFiles,
            handleSelect,
          }) => (
            <>
              <Modal.Body>
                <Tabs
                  variant="fullWidth"
                  ref={tabsRef}
                  onActiveTabChange={(tabIndex) =>
                    tabIndex === 0
                      ? handleTabChange("list")
                      : handleTabChange("upload")
                  }
                >
                  <Tabs.Item
                    active={activeTab === "list"}
                    title="My Files"
                    icon={FaFolderOpen}
                  >
                    <FileList />
                  </Tabs.Item>
                  <Tabs.Item
                    active={activeTab === "upload"}
                    title="Upload"
                    icon={GrCloudUpload}
                  >
                    <Uploader />
                  </Tabs.Item>
                </Tabs>
              </Modal.Body>
              {activeTab === "list" ? (
                <Modal.Footer className="flex items-center justify-between">
                  <Pagination
                    currentPage={pagination.currentPage}
                    totalPages={pagination.totalPages}
                    onPageChange={handlePageChange}
                    layout="navigation"
                    showIcons
                  />
                  {handleSelect && (
                    <Button
                      outline
                      color="green"
                      disabled={!selectedFiles.length && !handleSelect}
                    >
                      Select
                    </Button>
                  )}
                </Modal.Footer>
              ) : (
                <Modal.Footer className="flex items-center justify-between">
                  <Button
                    color="failure"
                    outline
                    onClick={() => handleSetUploads(null)}
                    className="w-full"
                    disabled={!uploads?.length}
                  >
                    Reset
                  </Button>
                  <Button
                    color="green"
                    outline
                    onClick={handleUpload}
                    className="w-full"
                    isProcessing={uploading}
                    disabled={!uploads?.length}
                  >
                    Upload {uploads?.length} File(s)
                  </Button>
                </Modal.Footer>
              )}
            </>
          )}
        </FileManagerContext.Consumer>
      </Modal>
    </FileManagerContextProvider>
  );
};
