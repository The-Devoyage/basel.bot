"use client";

import { Table } from "flowbite-react";
import { ShareableLinksTableHead } from "./components/shareable-links-table-head";
import { ShareableLink } from "@/types/shareable-link";
import { FC, useState } from "react";
import { LinkCell, StatusCell, UpdateLinkModal } from "./components";
import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";
dayjs.extend(utc);

interface ShareableLinksTableProps {
  shareableLinks: ShareableLink[] | null;
}

export const ShareableLinksTable: FC<ShareableLinksTableProps> = ({
  shareableLinks = [],
}) => {
  const [selectedLink, setSelectedLink] = useState<ShareableLink | null>(null);

  if (!shareableLinks?.length) {
    return null;
  }

  return (
    <Table hoverable>
      <ShareableLinksTableHead />
      <UpdateLinkModal
        show={!!selectedLink}
        shareableLink={selectedLink}
        onClose={() => setSelectedLink(null)}
      />
      <Table.Body className="divide-y">
        {shareableLinks?.map((sl) => (
          <Table.Row
            key={sl.uuid}
            className="cursor-pointer bg-white dark:border-gray-700 dark:bg-gray-800"
            onClick={() => setSelectedLink(sl)}
          >
            <Table.Cell>
              <StatusCell shareableLink={sl} />
            </Table.Cell>
            <Table.Cell className="hidden md:table-cell">{sl.views}</Table.Cell>
            <Table.Cell>{sl.tag || "--"}</Table.Cell>
            <Table.Cell>{sl.interviews.length || "--"}</Table.Cell>
            <Table.Cell className="hidden md:table-cell">
              {dayjs.utc(sl.created_at).local().format("MMM D, YYYY")}
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
