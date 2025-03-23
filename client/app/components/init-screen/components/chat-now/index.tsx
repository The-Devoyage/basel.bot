"use client";

import { Button } from "flowbite-react";
import { BiSolidLeaf } from "react-icons/bi";
import { useRouter, useSearchParams } from "next/navigation";

export const ChatNow = () => {
  const router = useRouter();
  const searchParams = useSearchParams();

  return (
    <Button
      color="green"
      className="w-full"
      onClick={() => router.push(`/chat?${searchParams.toString()}`)}
    >
      <BiSolidLeaf className="mr-2 size-5 text-green-400" />
      Chat Now
    </Button>
  );
};
