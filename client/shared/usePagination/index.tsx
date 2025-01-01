"use client";

import { useState } from "react";

export const usePagination = (limit: number = 10) => {
  const [pagination, setPagination] = useState({
    currentPage: 1,
    totalPages: 1,
    limit,
    offset: 0,
  });
  const nextOffset = (pagination.currentPage - 1) * pagination.limit;

  const handlePageChange = (page: number) => {
    setPagination({ ...pagination, currentPage: page, offset: 10 });
  };

  const handleSetTotal = (total: number = 0) => {
    setPagination({
      ...pagination,
      totalPages: Math.ceil((total || 0) / pagination.limit) || 1,
    });
  };

  return {
    pagination,
    handlePageChange,
    handleSetTotal,
    nextOffset,
  };
};
