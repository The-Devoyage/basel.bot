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
      body: { tag: "My Link" },
    },
    {
      successMessage: "Created Shareable Link",
      revalidationPath: Endpoint.ShareableLinks,
    },
  );

  const handleClick = async () => {
    call();
  };

  return (
    <Button color="success" onClick={handleClick} isProcessing={loading}>
      <BsPlusLg />
    </Button>
  );
};
