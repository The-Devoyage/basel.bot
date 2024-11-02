"use client";

import { useEffect, useState } from "react";
import { Table } from "flowbite-react";
import { getShareableLinks } from "@/api/shareable-links";
import { ShareableLink } from "@/types/shareable-link";
import { RiChatForwardFill } from "react-icons/ri";

export const ShareableLinksTable = () => {
  const [shareableLinks, setShareableLinks] = useState<ShareableLink[]>([]);

  useEffect(() => {
    const handleFetch = async () => {
      const response = await getShareableLinks();
      if (response.success && response.data) {
        setShareableLinks(response.data);
      }
    };
    handleFetch();
  }, []);

  return (
    <Table striped>
      <Table.Head>
        <Table.HeadCell>Tag</Table.HeadCell>
        <Table.HeadCell>Link</Table.HeadCell>
        <Table.HeadCell>Status</Table.HeadCell>
        <Table.HeadCell>Created At</Table.HeadCell>
      </Table.Head>
      <Table.Body className="divide-y">
        {shareableLinks.map((sl) => (
          <Table.Row key={sl.uuid}>
            <Table.Cell>{sl.tag || "--"}</Table.Cell>
            <Table.Cell>
              <RiChatForwardFill />
            </Table.Cell>
            <Table.Cell>{sl.status ? "Active" : "Inactive"}</Table.Cell>
            <Table.Cell>{sl.created_at}</Table.Cell>
          </Table.Row>
        ))}
      </Table.Body>
    </Table>
  );
};
