"use client";

import { Table } from "flowbite-react";
import { ShareableLinksTableHead } from "./components/shareable-links-table-head";
import { ShareableLink } from "@/types/shareable-link";
import { FC } from "react";
import { LinkCell, StatusCell, TagCell } from "./components";
import dayjs from "dayjs";

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
            <Table.Cell>
              <TagCell shareableLink={sl} />
            </Table.Cell>
            <Table.Cell>
              <StatusCell shareableLink={sl} />
            </Table.Cell>
            <Table.Cell className="hidden md:table-cell">
              {dayjs(sl.created_at).format("MMM D, YYYY")}
            </Table.Cell>
            <Table.Cell>
              <LinkCell shareableLink={sl} />
            </Table.Cell>
          </Table.Row>
        ))}
      </Table.Body>
    </Table>
  );
};
