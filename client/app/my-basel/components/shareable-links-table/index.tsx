"use client";
import { Table } from "flowbite-react";
import { ShareableLinksTableHead } from "./components/shareable-links-table-head";
import { ShareableLink } from "@/types/shareable-link";
import { FC } from "react";
import { LinkCell } from "./components";

interface ShareableLinksTableProps {
  shareableLinks: ShareableLink[] | null;
}

export const ShareableLinksTable: FC<ShareableLinksTableProps> = ({
  shareableLinks = [],
}) => {
  if (!shareableLinks?.length) {
    return null;
  }

  return (
    <Table striped>
      <ShareableLinksTableHead />
      <Table.Body className="divide-y">
        {shareableLinks?.map((sl) => (
          <Table.Row key={sl.uuid}>
            <Table.Cell>{sl.tag || "--"}</Table.Cell>
            <Table.Cell>{sl.status ? "Active" : "Inactive"}</Table.Cell>
            <Table.Cell>{sl.created_at}</Table.Cell>
            <Table.Cell>
              <LinkCell shareableLink={sl} />
            </Table.Cell>
          </Table.Row>
        ))}
      </Table.Body>
    </Table>
  );
};
