import { Table, TableBody, TableCell, TableRow } from "flowbite-react";
import { ShareableLinksTableHead } from "./components/shareable-links-table-head";
import { ShareableLink } from "@/types/shareable-link";
import { FC } from "react";
import { LinkCell, StatusCell, TagCell } from "./components";
import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";
dayjs.extend(utc);

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
    <Table>
      <ShareableLinksTableHead />
      <TableBody className="divide-y">
        {shareableLinks?.map((sl) => (
          <TableRow
            key={sl.uuid}
            className="bg-white dark:border-gray-700 dark:bg-gray-800"
          >
            <TableCell>
              <StatusCell shareableLink={sl} />
            </TableCell>
            <TableCell>{sl.views}</TableCell>
            <TableCell>
              <TagCell shareableLink={sl} />
            </TableCell>
            <TableCell className="hidden md:table-cell">
              {dayjs.utc(sl.created_at).local().format("MMM D, YYYY")}
            </TableCell>
            <TableCell>
              <LinkCell shareableLink={sl} />
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};
