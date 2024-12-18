"use client";

import { Endpoint } from "@/api";
import { useCallApi } from "@/shared/useCallApi";
import { ShareableLink } from "@/types/shareable-link";
import { Button, Modal, TextInput } from "flowbite-react";
import { FC, useEffect, useRef, useState } from "react";
import { IoMdCheckbox } from "react-icons/io";

interface TagCellProps {
  shareableLink: ShareableLink;
}

export const TagCell: FC<TagCellProps> = ({ shareableLink }) => {
  const [tag, setTag] = useState("");
  const [visible, setVisible] = useState(false);
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

  const handleVisibleChange = () => {
    setVisible(true);
  };

  const handleSave = async () => {
    await call();
  };

  return (
    <div className="flex">
      <Modal show={visible} onClose={() => setVisible(false)}>
        <Modal.Header className="py-3">Tag</Modal.Header>
        <Modal.Body>
          <div className="flex w-full gap-2">
            <TextInput
              placeholder="Tag your link..."
              disabled={loading}
              value={tag}
              ref={inputRef}
              onChange={(e) => setTag(e.currentTarget.value)}
              className="w-full"
              onFocus={() => setVisible(true)}
            />
            <Button className="flex items-center" onClick={handleSave}>
              <IoMdCheckbox className="h-4 w-4" />
            </Button>
          </div>
        </Modal.Body>
      </Modal>
      <Button
        onClick={handleVisibleChange}
        color="light"
        className="w-full"
        isProcessing={loading}
      >
        {tag || "--"}
      </Button>
    </div>
  );
};
