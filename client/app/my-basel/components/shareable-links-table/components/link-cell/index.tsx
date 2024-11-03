"use client";

import { ShareableLink } from "@/types/shareable-link";
import { Button, TextInput, Tooltip } from "flowbite-react";
import { FC } from "react";
import { BiSolidCopy } from "react-icons/bi";

interface LinkCellProps {
  shareableLink: ShareableLink;
}

export const LinkCell: FC<LinkCellProps> = ({ shareableLink }) => {
  const handleCopy = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
    } catch (err) {
      console.error(err);
      return false;
    }
  };

  return (
    <span className="flex space-x-1">
      <TextInput readOnly value={shareableLink.link} className="w-full" />
      <Tooltip content="Copied!" trigger="click">
        <Button
          onClick={() => handleCopy(shareableLink.link)}
          className="h-full"
        >
          <BiSolidCopy />
        </Button>
      </Tooltip>
    </span>
  );
};
