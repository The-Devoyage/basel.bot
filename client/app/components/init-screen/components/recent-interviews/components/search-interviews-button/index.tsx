"use client";

import { Button } from "flowbite-react";
import { useContext } from "react";
import { GlobalContext } from "@/app/provider";
import { useRouter } from "next/navigation";

export const SearchInterviewsButton = () => {
  const router = useRouter();
  const {
    store: {
      auth: { shareableLink },
    },
  } = useContext(GlobalContext);

  if (shareableLink) return null;

  return (
    <Button
      outline
      gradientDuoTone="purpleToBlue"
      className="w-full"
      onClick={() => router.push("/interviews")}
    >
      Search Interviews
    </Button>
  );
};
