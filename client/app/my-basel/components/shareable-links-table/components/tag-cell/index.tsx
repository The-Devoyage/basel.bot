"use client";

import { Endpoint } from "@/api";
import { useCallApi } from "@/shared/useCallApi";
import { ShareableLink } from "@/types/shareable-link";
import { TextInput } from "flowbite-react";
import { FC, useEffect, useRef, useState } from "react";

interface TagCellProps {
  shareableLink: ShareableLink;
}

export const TagCell: FC<TagCellProps> = ({ shareableLink }) => {
  const [tag, setTag] = useState("");
  const inputRef = useRef<HTMLInputElement | null>(null);

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
      onSuccess: () => {
        setTimeout(() => {
          inputRef.current?.focus();
        }, 300);
      },
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
      ref={inputRef}
      onChange={(e) => setTag(e.currentTarget.value)}
    />
  );
};
