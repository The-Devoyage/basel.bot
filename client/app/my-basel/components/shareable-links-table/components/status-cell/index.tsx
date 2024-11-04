"use client";

import { Endpoint } from "@/api";
import { useCallApi } from "@/shared/useCallApi";
import { ShareableLink } from "@/types/shareable-link";
import { Button, Tooltip } from "flowbite-react";
import { FC } from "react";
import { FaUnlink, FaLink } from "react-icons/fa";

interface StatusCellProps {
  shareableLink: ShareableLink;
}

export const StatusCell: FC<StatusCellProps> = ({ shareableLink }) => {
  const { call, loading } = useCallApi(
    {
      endpoint: Endpoint.UpdateShareableLink,
      method: "PATCH",
      path: {
        uuid: shareableLink.uuid,
      },
      body: {
        status: !shareableLink.status,
      },
      query: null,
    },
    {
      successMessage: "Updated Shareable Link",
      revalidationPath: Endpoint.ShareableLinks,
    },
  );
  const handleClick = async () => {
    await call();
  };
  return (
    <Tooltip
      content={shareableLink.status ? "Deactivate Link" : "Activate Link"}
    >
      <Button
        className="px-2"
        onClick={handleClick}
        isProcessing={loading}
        color={shareableLink.status ? "success" : "gray"}
      >
        {shareableLink.status ? <FaLink /> : <FaUnlink />}
      </Button>
    </Tooltip>
  );
};
