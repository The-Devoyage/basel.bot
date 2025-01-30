"use client";

import { Endpoint } from "@/api";
import { useCallApi } from "@/shared/useCallApi";
import { ShareableLink } from "@/types/shareable-link";
import { ToggleSwitch } from "flowbite-react";
import { FC } from "react";

interface StatusCellProps {
  shareableLink: ShareableLink;
}

export const StatusCell: FC<StatusCellProps> = ({ shareableLink }) => {
  const { call } = useCallApi(
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
      toast: {
        onSuccess: true,
      },
      callApiOptions: {
        revalidationTag: "shareable-links",
      },
    },
  );

  const handleChange = async () => {
    await call();
  };

  return (
    <div onClick={(e) => e.stopPropagation()}>
      <ToggleSwitch
        checked={shareableLink.status}
        onChange={handleChange}
        color="green"
      />
    </div>
  );
};
