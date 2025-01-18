"use client";

import { Endpoint } from "@/api";
import { useCallApi } from "@/shared/useCallApi";
import { Button } from "flowbite-react";
import { BsPlusLg } from "react-icons/bs";

export const CreateShareableLinkButton = () => {
  const { call, loading } = useCallApi(
    {
      endpoint: Endpoint.CreateShareableLink,
      method: "POST",
      query: null,
      body: null,
      path: null,
    },
    {
      successMessage: "Created Shareable Link",
      callApiOptions: {
        revalidationTag: "get-shareable-links",
      },
    },
  );

  const handleClick = async () => {
    await call();
  };

  return (
    <Button
      outline
      gradientDuoTone="purpleToBlue"
      onClick={handleClick}
      isProcessing={loading}
    >
      <BsPlusLg />
    </Button>
  );
};
