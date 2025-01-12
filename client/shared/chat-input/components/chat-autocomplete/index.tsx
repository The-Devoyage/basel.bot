"use client";

import { Button, Tooltip } from "flowbite-react";
import { PiLightningDuotone } from "react-icons/pi";
import { Endpoint } from "@/api";
import {
  Dispatch,
  FC,
  SetStateAction,
  useContext,
  useEffect,
  useState,
} from "react";
import { useCallApi } from "@/shared/useCallApi";
import clsx from "clsx";
import { GlobalContext } from "@/app/provider";
import { GrSend } from "react-icons/gr";
import { HiOutlineChevronLeft, HiOutlineChevronRight } from "react-icons/hi";

export const ChatAutocomplete: FC<{
  setMessageText: Dispatch<SetStateAction<string>>;
  messageText: string;
  handleMessage: () => void;
}> = ({ setMessageText, messageText, handleMessage }) => {
  const className = "h-4 w-4";
  const { call, res, loading } = useCallApi({
    endpoint: Endpoint.GetSuggestion,
    query: null,
    body: null,
    path: null,
  });
  const { client } = useContext(GlobalContext);

  useEffect(() => {
    if (res?.data?.text) {
      setMessageText(res.data.text);
    }
  }, [res]);

  const handleClick = () => {
    call();
  };

  return (
    <Button.Group className="m-2">
      <Button
        onClick={handleClick}
        disabled={!client?.messages.length}
        outline
        isProcessing={loading}
        color="yellow"
        className="text-slate-400 hover:text-yellow-300"
      >
        <PiLightningDuotone className={className} />
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
  );
};
