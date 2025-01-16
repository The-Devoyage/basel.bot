import {
  FC,
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import { useCallApi } from "../useCallApi";
import { Endpoint } from "@/api";
import { GlobalContext } from "@/app/provider";
import { addToast } from "../useStore/toast";
import { File } from "@/types";
import { usePagination } from "../usePagination";
import { TabsRef } from "flowbite-react";

interface FileManagerContext {
  handleUpload: () => Promise<void>;
  uploads: FileList | null;
  handleSetUploads: (files: FileList | null) => void;
  uploading: boolean;
  downloading: string | null;
  files: File[];
  pagination: ReturnType<typeof usePagination>["pagination"];
  handlePageChange: ReturnType<typeof usePagination>["handlePageChange"];
  activeTab: "list" | "upload";
  handleTabChange: (tab: "list" | "upload") => void;
  selectedFiles: File[];
  handleSelectFile: (file: File) => void;
  handleDownloadFile: (file: File) => Promise<void>;
  multiple: boolean;
  handleSelect?: (files: File[]) => void;
}

export const FileManagerContext = createContext<FileManagerContext>({
  handleUpload: async () => Promise.resolve(),
  uploads: null,
  handleSetUploads: () => null,
  uploading: false,
  downloading: null,
  files: [],
  pagination: { limit: 10, offset: 0, currentPage: 1, totalPages: 1 },
  handlePageChange: () => null,
  activeTab: "list",
  handleTabChange: () => null,
  selectedFiles: [],
  handleSelectFile: () => null,
  handleDownloadFile: () => Promise.resolve(),
  multiple: false,
});

export const FileManagerContextProvider: FC<{
  children: React.ReactNode;
  show: boolean;
  tabsRef: TabsRef | null;
  multiple?: boolean;
  onSelect?: (files: File[]) => void;
}> = ({ children, show, tabsRef, multiple, onSelect }) => {
  const {
    dispatch,
    store: { isAuthenticated },
  } = useContext(GlobalContext);
  const [activeTab, setActiveTab] = useState<"list" | "upload">("list");
  const [uploads, setUploads] = useState<FileList | null>(null);
  const [uploading, setUploading] = useState(false);
  const [downloading, setDownloading] = useState<string | null>(null);
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const uploadLinkRes = useCallApi({
    endpoint: Endpoint.GetFileUploadLink,
    query: { file_name: "abcdedfg.jpg", file_size: 0, mimetype: "" },
    body: null,
    path: null,
  });
  const activateFile = useCallApi({
    endpoint: Endpoint.ActivateFile,
    method: "PATCH",
    query: null,
    body: { uuid: "" },
    path: null,
  });
  const downloadLinkRes = useCallApi({
    endpoint: Endpoint.GetFileDownloadLink,
    query: { uuid: "" },
    body: null,
    path: null,
  });
  const { pagination, handlePageChange, handleSetTotal, nextOffset } =
    usePagination();
  const getFilesRes = useCallApi(
    {
      endpoint: Endpoint.GetFiles,
      query: {
        limit: pagination.limit,
        offset: nextOffset,
      },
      path: null,
      body: null,
    },
    {
      callOnMount: isAuthenticated || false,
      onSuccess: async (res) => {
        handleSetTotal(res?.total);
      },
    },
  );
  const files = getFilesRes.res?.data || [];

  useEffect(() => {
    if (!isAuthenticated || !show) return;

    handleFetch();
  }, [pagination.currentPage, show]);

  useEffect(() => {
    if (activeTab === "list") {
      handlePageChange(1);
      getFilesRes.call({
        query: { limit: 10, offset: 0 },
        body: null,
        path: null,
      });
    }
    tabsRef?.setActiveTab(activeTab === "list" ? 0 : 1);
  }, [activeTab]);

  const handleSetUploads = (files: FileList | null) => {
    setUploads(files);
  };

  const handleFetch = async () => {
    await getFilesRes.call();
  };

  const handleUpload = async () => {
    if (!uploads?.length) return;
    setUploading(true);
    const files = Array.from(uploads);

    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      try {
        const res = await uploadLinkRes.call({
          query: {
            file_name: file.name,
            file_size: file.size,
            mimetype: file.type,
          },
          body: null,
          path: null,
        });

        if (!res?.success || !res.data) return;

        const uploadResponse = await fetch(res.data.upload_link, {
          method: "PUT",
          body: file,
          headers: {
            "Content-Type": file.type,
          },
        });

        if (!uploadResponse.ok) {
          dispatch(
            addToast({
              type: "error",
              title: "Upload Failed",
              description: "Failed to upload the file.",
            }),
          );
          throw new Error("Failed to upload file.");
        }

        await activateFile.call({
          body: {
            uuid: res.data.file_uuid,
          },
          path: null,
          query: null,
        });
      } catch (error) {
        console.error(error);
      }
    }
    setUploading(false);
    handleSetUploads(null);
    handleTabChange("list");
    dispatch(
      addToast({
        type: "success",
        description: "Added file(s) to your file manager.",
      }),
    );
  };

  const handleTabChange = (tab: "list" | "upload") => {
    setActiveTab(tab);
  };

  const handleSelectFile = (file: File) => {
    if (selectedFiles.findIndex((f) => f.uuid === file.uuid) > -1) {
      return setSelectedFiles((curr) => [
        ...curr.filter((f) => f.uuid !== file.uuid),
      ]);
    }
    if (selectedFiles.length && !multiple) {
      dispatch(
        addToast({
          type: "error",
          description: "You may only select a single file.",
        }),
      );
      return;
    }
    setSelectedFiles((curr) => [...curr, file]);
  };

  const handleDownloadFile = async (file: File) => {
    try {
      setDownloading(file.uuid);
      // Get the presigned URL
      const downloadLink = await downloadLinkRes.call({
        query: { uuid: file.uuid },
        path: null,
        body: null,
      });

      if (downloadLink?.data?.download_link) {
        const response = await fetch(downloadLink.data.download_link);
        const blob = await response.blob();

        // Create a Blob URL
        const blobUrl = window.URL.createObjectURL(blob);

        // Trigger download
        const anchor = document.createElement("a");
        anchor.href = blobUrl;
        anchor.download = file.file_name;
        document.body.appendChild(anchor);
        anchor.click();
        document.body.removeChild(anchor);

        // Revoke the Blob URL
        window.URL.revokeObjectURL(blobUrl);
        setDownloading(null);
      } else {
        console.error("Download link not available");
        setDownloading(null);
      }
    } catch (error) {
      setDownloading(null);
      console.error("Failed to download file:", error);
    }
  };

  const handleSelect = () => {
    onSelect?.(selectedFiles);
  };

  const value = useMemo(
    () => ({
      handleSetUploads,
      handleUpload,
      uploads,
      uploading: uploading || activateFile.loading,
      files,
      pagination,
      handlePageChange,
      activeTab,
      handleTabChange,
      handleSelectFile,
      selectedFiles,
      handleDownloadFile,
      downloading,
      multiple: !!multiple,
      handleSelect: onSelect && handleSelect,
    }),
    [
      uploads,
      handleSetUploads,
      handleUpload,
      files,
      pagination,
      handlePageChange,
      activeTab,
      selectedFiles,
      downloading,
    ],
  );

  return (
    <FileManagerContext.Provider value={value}>
      {children}
    </FileManagerContext.Provider>
  );
};
