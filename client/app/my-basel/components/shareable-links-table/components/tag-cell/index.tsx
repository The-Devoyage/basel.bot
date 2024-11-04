"use client";

import { Endpoint } from "@/api";
import { useCallApi } from "@/shared/useCallApi";
import { ShareableLink } from "@/types/shareable-link";
import { TextInput } from "flowbite-react";
import { FC, useEffect, useState } from "react";

interface TagCellProps {
  shareableLink: ShareableLink;
}

export const TagCell: FC<TagCellProps> = ({ shareableLink }) => {
  const [tag, setTag] = useState("");

  const { call, loading } = useCallApi(
    {
      endpoint: Endpoint.UpdateShareableLink,
      method: "PATCH",
      path: {
        uuid: shareableLink.uuid,
      },
      body: {
        tag,
      },
      query: null,
    },
    {
      successMessage: "Updated Shareable Link",
      revalidationPath: Endpoint.ShareableLinks,
    },
  );

  useEffect(() => {
    if (shareableLink) setTag(shareableLink.tag);
  }, [shareableLink]);

  useEffect(() => {
    const timeout = setTimeout(async () => {
      if (tag !== shareableLink.tag && !loading) {
        await call();
      }
    }, 500);

    return () => clearTimeout(timeout);
  }, [tag]);

  return (
    <TextInput
      placeholder="Tag your link..."
      disabled={loading}
      value={tag}
      onChange={(e) => setTag(e.currentTarget.value)}
    />
  );
};
