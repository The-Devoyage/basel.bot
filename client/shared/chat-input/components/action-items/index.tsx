"use client";

import { Button } from "flowbite-react";
import { PiLightningDuotone } from "react-icons/pi";
import { Endpoint } from "@/api";
import {
  Dispatch,
  FC,
  RefObject,
  SetStateAction,
  useContext,
  useEffect,
  useState,
} from "react";
import { useCallApi } from "@/shared/useCallApi";
import { GlobalContext } from "@/app/provider";
import { GrSend } from "react-icons/gr";
import { TiAttachmentOutline } from "react-icons/ti";
import { FileManager } from "@/shared/file-manager";
import { File } from "@/types";
import { ChatInputContext } from "../../context";
import { ValidMimeType } from "@/types";
import { Tooltip } from "react-tooltip";

export const ActionItems: FC<{
  setMessageText: Dispatch<SetStateAction<string>>;
  messageText: string;
  handleMessage: () => void;
  inputRef: RefObject<HTMLTextAreaElement>;
}> = ({ setMessageText, messageText, handleMessage, inputRef }) => {
  const { setFiles } = useContext(ChatInputContext);
  const className = "h-4 w-4";
  const [show, setShow] = useState(false);
  const { call, res, loading } = useCallApi({
    endpoint: Endpoint.GetSuggestion,
    query: null,
    body: null,
    path: null,
  });
  const {
    client,
    store: {
      auth: { isAuthenticated },
    },
  } = useContext(GlobalContext);

  useEffect(() => {
    if (res?.data?.text) {
      setMessageText(res.data.text);
    }
  }, [res]);

  const handleAutoComplete = () => {
    call();
  };

  const handleSelectFiles = (files: File[]) => {
    inputRef.current?.focus();
    setFiles(files);
  };

  return (
    <>
      <FileManager
        show={show}
        onClose={() => setShow(false)}
        onSelect={handleSelectFiles}
        validMimeTypes={[
          ValidMimeType.PDF,
          ValidMimeType.TEXT_PLAIN,
          ValidMimeType.MS_WORD_DOCX,
        ]}
      />
      <Tooltip id="auto-complete" />
      <Tooltip id="attach-files" />
      <Button.Group className="m-2">
        <Button
          onClick={handleAutoComplete}
          disabled={!client?.messages.length || !isAuthenticated}
          outline
          isProcessing={loading}
          color="yellow"
          className="text-slate-400 hover:text-slate-800"
          data-tooltip-id="auto-complete"
          data-tooltip-content="Auto Complete"
        >
          <PiLightningDuotone className={className} />
        </Button>
        <Button
          onClick={() => setShow(true)}
          outline
          color="light"
          className="border-none text-slate-700"
          disabled={!isAuthenticated}
          data-tooltip-id="attach-files"
          data-tooltip-content="Attach Files"
        >
          <TiAttachmentOutline className={className} />
        </Button>
        <Button
          outline
          color="green"
          className="h-full"
          onClick={() => {
            handleMessage();
          }}
          disabled={!messageText || client?.loading}
          isProcessing={client?.loading}
        >
          <GrSend className={className} />
        </Button>
      </Button.Group>
    </>
  );
};
