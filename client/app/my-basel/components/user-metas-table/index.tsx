"use client";

import { Endpoint } from "@/api";
import dayjs from "dayjs";
import {
  Pagination,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeadCell,
  TableRow,
} from "flowbite-react";
import { DeleteCell, StatusCell } from "./components";
import { useCallApi } from "@/shared/useCallApi";
import { useCallback, useEffect } from "react";
import utc from "dayjs/plugin/utc";
import { usePagination } from "@/shared/usePagination";
dayjs.extend(utc);

export const UserMetasTable = () => {
  const { pagination, handlePageChange, handleSetTotal, nextOffset } =
    usePagination();
  const { call, res } = useCallApi(
    {
      endpoint: Endpoint.GetUserMetas,
      body: null,
      path: null,
      query: {
        limit: pagination.limit,
        offset: nextOffset,
      },
    },
    {
      onSuccess: (res) => {
        handleSetTotal(res.total);
      },
    },
  );

  const handleFetch = useCallback(async () => {
    await call();
  }, [call]);

  useEffect(() => {
    handleFetch();
  }, [pagination.currentPage, handleFetch]);

  return (
    <div className="relative">
      <Table className="mb-0" striped>
        <TableHead>
          <TableHeadCell>Status</TableHeadCell>
          <TableHeadCell>Meta</TableHeadCell>
          <TableHeadCell className="hidden md:table-cell">
            Created At
          </TableHeadCell>
          <TableHeadCell>Delete</TableHeadCell>
        </TableHead>
        <TableBody>
          {res?.data?.map((meta) => (
            <TableRow
              key={meta.uuid}
              className="bg-white dark:border-gray-700 dark:bg-gray-800"
            >
              <TableCell>
                <StatusCell userMeta={meta} refetch={call} />
              </TableCell>
              <TableCell>{meta.data}</TableCell>
              <TableCell className="hidden md:table-cell">
                {dayjs.utc(meta.created_at).local().format("MMM D, YYYY")}
              </TableCell>
              <TableCell>
                <DeleteCell userMeta={meta} refetch={call} />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <div className="mb-6 flex justify-end">
        <Pagination
          currentPage={pagination.currentPage}
          totalPages={pagination.totalPages}
          onPageChange={handlePageChange}
        />
      </div>
    </div>
  );
};
