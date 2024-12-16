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
import { StatusCell } from "./components";
import { useCallApi } from "@/shared/useCallApi";
import { useEffect, useState } from "react";
import utc from "dayjs/plugin/utc";
import { Loader } from "@/shared/loader";
dayjs.extend(utc);

export const UserMetasTable = () => {
  const [pagination, setPagination] = useState({
    currentPage: 1,
    totalPages: 1,
    limit: 10,
    offset: 0,
  });

  const { call, loading, res } = useCallApi(
    {
      endpoint: Endpoint.GetUserMetas,
      body: null,
      path: null,
      query: {
        limit: pagination.limit,
        offset: (pagination.currentPage - 1) * pagination.limit,
      },
    },
    {
      onSuccess: (res) => {
        console.log(res);
        setPagination({
          ...pagination,
          totalPages: Math.ceil((res.total || 0) / pagination.limit),
        });
      },
    },
  );

  const handleFetch = async () => {
    await call();
  };

  useEffect(() => {
    handleFetch();
  }, [pagination.currentPage]);

  const handlePageChange = (page: number) => {
    setPagination({ ...pagination, currentPage: page, offset: 10 });
  };

  return (
    <div className="relative">
      <Table className="mb-0" striped>
        <TableHead>
          <TableHeadCell>Status</TableHeadCell>
          <TableHeadCell>Meta</TableHeadCell>
          <TableHeadCell className="hidden md:table-cell">
            Created At
          </TableHeadCell>
        </TableHead>
        <TableBody>
          {res?.data?.map((meta) => (
            <TableRow className="bg-white dark:border-gray-700 dark:bg-gray-800">
              <TableCell>
                <StatusCell userMeta={meta} refetch={call} />
              </TableCell>
              <TableCell>{meta.data}</TableCell>
              <TableCell className="hidden md:table-cell">
                {dayjs.utc(meta.created_at).local().format("MMM D, YYYY")}
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
