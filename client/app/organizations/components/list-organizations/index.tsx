"use client";

import { Button, Card, Pagination, Table, Tooltip } from "flowbite-react";
import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";
import { useRouter } from "next/navigation";
import { Typography } from "@/shared/typography";
import { Loader } from "@/shared/loader";
import { OrganizationsPageContext } from "../../context";
import { useContext } from "react";
import { MdOutlineEdit } from "react-icons/md";
import { useCheckPerm } from "@/utils/useCheckPerm";
import { SubscriptionFeature } from "@/types";

dayjs.extend(utc);

export const ListOrganizations = () => {
  const router = useRouter();
  const {
    organizations,
    loading,
    pager,
    setSelectedOrganization,
    toggleEditOrganizationModal,
  } = useContext(OrganizationsPageContext);
  const allowEdit = useCheckPerm(SubscriptionFeature.MANAGE_ORGANIZATION);

  if (loading) {
    return (
      <Card>
        <Loader />
      </Card>
    );
  }

  if (!organizations || !organizations.length) {
    return (
      <Card>
        <Typography.Heading className="text-xl">
          Nothing Found!
        </Typography.Heading>
        <Typography.Paragraph>
          Create an organization to get started.
        </Typography.Paragraph>
      </Card>
    );
  }

  return (
    <>
      <Table hoverable>
        <Table.Head>
          <Table.HeadCell>Name</Table.HeadCell>
          <Table.HeadCell className="hidden md:table-cell">
            Status
          </Table.HeadCell>
          <Table.HeadCell className="hidden md:table-cell">
            Created At
          </Table.HeadCell>
          <Table.HeadCell className="text-center">Edit</Table.HeadCell>
        </Table.Head>
        <Table.Body>
          {organizations.map((o) => (
            <Table.Row
              key={o.uuid}
              className="cursor-pointer bg-white dark:border-gray-700 dark:bg-gray-800"
              onClick={() =>
                router.push(
                  `/organizations/${o.name.replaceAll(" ", "-").toLowerCase()}`,
                )
              }
            >
              <Table.Cell>{o.name}</Table.Cell>
              <Table.Cell className="hidden md:table-cell">
                {o.status ? "Active" : "Disabled"}
              </Table.Cell>
              <Table.Cell className="hidden md:table-cell">
                {dayjs.utc(o.created_at).local().format("MMM D YYYY h:mma")}
              </Table.Cell>
              <Table.Cell
                className="flex items-center justify-center"
                onClick={(e) => e.stopPropagation()}
              >
                <Tooltip
                  content={
                    !allowEdit && "Upgrade to edit organization details."
                  }
                >
                  <Button
                    color="success"
                    outline
                    disabled={!allowEdit}
                    onClick={() => {
                      toggleEditOrganizationModal();
                      setSelectedOrganization(o);
                    }}
                  >
                    <MdOutlineEdit className="size-4" />
                  </Button>
                </Tooltip>
              </Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table>
      <div className="flex justify-end">
        <Pagination
          currentPage={pager?.pagination.currentPage || 0}
          totalPages={pager?.pagination.totalPages || 0}
          onPageChange={(p) => pager?.handlePageChange(p)}
        />
      </div>
    </>
  );
};
