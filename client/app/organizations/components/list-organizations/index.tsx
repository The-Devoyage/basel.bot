"use client";

import { Button, Card, Pagination, Table } from "flowbite-react";
import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";
import { useRouter } from "next/navigation";
import { Typography } from "@/shared/typography";
import { Loader } from "@/shared/loader";
import { OrganizationsPageContext } from "../../context";
import { useContext } from "react";

dayjs.extend(utc);

export const ListOrganizations = () => {
  const router = useRouter();
  const { organizations, loading } = useContext(OrganizationsPageContext);

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
          <Table.HeadCell>Status</Table.HeadCell>
          <Table.HeadCell>Created At</Table.HeadCell>
          <Table.HeadCell className="text-center">Leave</Table.HeadCell>
        </Table.Head>
        <Table.Body>
          {organizations.map((o) => (
            <Table.Row
              className="cursor-pointer bg-white dark:border-gray-700 dark:bg-gray-800"
              onClick={() =>
                router.push(
                  `/organizations/${o.name.replaceAll(" ", "-").toLowerCase()}`,
                )
              }
            >
              <Table.Cell>{o.name}</Table.Cell>
              <Table.Cell>{o.status ? "Active" : "Disabled"}</Table.Cell>
              <Table.Cell>
                {dayjs.utc(o.created_at).local().format("MMM D YYYY h:mma")}
              </Table.Cell>
              <Table.Cell
                className="flex items-center justify-center"
                onClick={(e) => e.stopPropagation()}
              >
                <Button color="failure" outline>
                  Leave
                </Button>
              </Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table>
      <div className="flex justify-end">
        <Pagination currentPage={0} totalPages={0} onPageChange={() => null} />
      </div>
    </>
  );
};
