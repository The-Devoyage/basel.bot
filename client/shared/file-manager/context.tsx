import { FC, createContext, useMemo, useState } from "react";
import { useCallApi } from "../useCallApi";
import { Endpoint } from "@/api";

interface FileManagerContext {
  handleUpload: () => Promise<void>;
  uploads: FileList | null;
  handleSetUploads: (files: FileList | null) => void;
}

export const FileManagerContext = createContext<FileManagerContext>({
  handleUpload: async () => Promise.resolve(),
  uploads: null,
  handleSetUploads: () => null,
});

export const FileManagerContextProvider: FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [uploads, setUploads] = useState<FileList | null>(null);
  const uploadLinkRes = useCallApi({
    endpoint: Endpoint.GetFileUploadLink,
    query: { file_name: "abcdedfg.jpg", file_size: 1024 },
    body: null,
    path: null,
  });

  const handleSetUploads = (files: FileList | null) => {
    setUploads(files);
  };

  const handleUpload = async () => {
    if (!uploads?.length) return;
    const files = Array.from(uploads);

    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const res = await uploadLinkRes.call({
        query: { file_name: file.name, file_size: file.size },
        body: null,
        path: null,
      });
      console.log(res);
    }
  };

  const value = useMemo(
    () => ({ handleSetUploads, handleUpload, uploads }),
    [uploads, handleSetUploads, handleUpload],
  );

  return (
    <FileManagerContext.Provider value={value}>
      {children}
    </FileManagerContext.Provider>
  );
};
