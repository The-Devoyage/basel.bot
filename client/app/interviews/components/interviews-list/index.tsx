"use client";

import { Endpoint } from "@/api";
import { useCallApi } from "@/shared/useCallApi";
import { Button, Pagination, TextInput, ToggleSwitch } from "flowbite-react";
import { useState, useEffect, useContext } from "react";
import { InterviewListResults } from "./components";
import { usePagination } from "@/shared/usePagination";
import { GlobalContext } from "@/app/provider";

export const InterviewsList = () => {
  const [takenByMe, setTakenByMe] = useState(false);
  const {
    store: {
      auth: { isAuthenticated },
    },
  } = useContext(GlobalContext);
  const [searchTerm, setSearchTerm] = useState<string | undefined>();
  const { pagination, handlePageChange, handleSetTotal, nextOffset } =
    usePagination();
  const { res, loading, call } = useCallApi(
    {
      endpoint: Endpoint.GetInterviews,
      query: {
        limit: pagination.limit,
        offset: nextOffset,
        taken_by_me: takenByMe,
        search_term: searchTerm,
      },
      body: null,
      path: null,
    },
    {
      callOnMount: true,
      onSuccess: async (res) => {
        handleSetTotal(res?.total);
      },
    },
  );

  useEffect(() => {
    call();
  }, [takenByMe, pagination.currentPage]);

  const handleSearch = () => {
    call({
      query: {
        limit: pagination.limit,
        offset: nextOffset,
        taken_by_me: takenByMe,
        search_term: searchTerm,
      },
      body: null,
      path: null,
    });
  };

  return (
    <>
      <div className="flex flex-col gap-2 md:flex-row">
        {isAuthenticated && (
          <div className="order-2 flex w-full items-center justify-center rounded-md border-2 border-purple-300 p-2 md:order-first md:w-1/4">
            <ToggleSwitch
              checked={takenByMe}
              onChange={(c) => setTakenByMe(c)}
              label="Taken by Me"
              color="purple"
            />
          </div>
        )}
        <TextInput
          placeholder="Search for Interviews"
          name="search_term"
          className="w-full"
          onChange={(e) => setSearchTerm(e.currentTarget.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              handleSearch();
            }
          }}
        />
        <Button
          outline
          gradientMonochrome="purple"
          type="submit"
          onClick={handleSearch}
          className="order-last"
        >
          Search
        </Button>
      </div>
      <InterviewListResults interviews={res?.data || []} loading={loading} />
      <div className="flex justify-center">
        <Pagination
          currentPage={pagination.currentPage}
          totalPages={pagination.totalPages}
          onPageChange={handlePageChange}
          showIcons
        />
      </div>
    </>
  );
};
