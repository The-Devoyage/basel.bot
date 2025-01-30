"use client";

import { Table } from "flowbite-react";

export const ShareableLinksTableHead = () => (
  <Table.Head>
    <Table.HeadCell>Status</Table.HeadCell>
    <Table.HeadCell className="hidden md:table-cell">Views</Table.HeadCell>
    <Table.HeadCell>Tag</Table.HeadCell>
    <Table.HeadCell>Interviews</Table.HeadCell>
    <Table.HeadCell className="hidden md:table-cell">Created At</Table.HeadCell>
    <Table.HeadCell>Link</Table.HeadCell>
  </Table.Head>
);
