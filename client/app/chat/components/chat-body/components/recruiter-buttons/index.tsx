"use client";

import { useHandleMessage } from "@/app/components/init-screen/components";
import { GlobalContext } from "@/app/provider";
import { Button } from "flowbite-react";
import { useRouter, useSearchParams } from "next/navigation";
import { useContext } from "react";

export const RecruiterButtons = () => {
  const { handleMessage } = useHandleMessage();
  const { slToken } = useContext(GlobalContext);
  const router = useRouter();
  const searchParams = useSearchParams();

  return (
    <div className="flex gap-2">
      <Button
        gradientDuoTone="greenToBlue"
        outline
        onClick={() =>
          handleMessage(
            "generate_resume",
            null,
            "Only provide information that has been supplied by the candidate.",
          )
        }
        className="mt-4 w-full"
      >
        Resume
      </Button>
      {slToken && (
        <Button
          gradientDuoTone="purpleToBlue"
          outline
          onClick={() => router.push(`/?${searchParams.toString()}`)}
          className="mt-4 w-full"
        >
          Profile
        </Button>
      )}
    </div>
  );
};
