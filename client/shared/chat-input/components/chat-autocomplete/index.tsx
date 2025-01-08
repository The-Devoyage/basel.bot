"use client";

import { Button, Tooltip } from "flowbite-react";
import { PiLightningDuotone } from "react-icons/pi";
import { Endpoint } from "@/api";
import { Dispatch, FC, SetStateAction, useEffect } from "react";
import { useCallApi } from "@/shared/useCallApi";
import clsx from "clsx";

export const ChatAutocomplete: FC<{
  setMessageText: Dispatch<SetStateAction<string>>;
}> = ({ setMessageText }) => {
  const { call, res, loading } = useCallApi({
    endpoint: Endpoint.GetSuggestion,
    query: null,
    body: null,
    path: null,
  });

  useEffect(() => {
    if (res?.data?.text) {
      setMessageText(res.data.text);
    }
  }, [res]);

  const handleClick = () => {
    call();
  };

  return (
    <div className="absolute bottom-0 right-0 z-50">
      <Tooltip content="Suggest a Response." placement="top">
        <button
          onClick={handleClick}
          className={clsx(
            "p-3 text-slate-400 hover:text-slate-600 dark:hover:text-white",
            {
              "animate-shake animate-bounce": loading,
            },
          )}
        >
          <PiLightningDuotone className="h-6 w-6" />
        </button>
      </Tooltip>
    </div>
  );
};
