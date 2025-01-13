"use client";

import { Button, Card, Checkbox, Modal, Table } from "flowbite-react";
import { FaShare } from "react-icons/fa";

export const FileList = () => {
  return (
    <Modal.Body className="h-96">
      <Card>
        <Table>
          <Table.Head>
            <Table.HeadCell>
              <Checkbox />
            </Table.HeadCell>
            <Table.HeadCell>File Name</Table.HeadCell>
            <Table.HeadCell>Created At</Table.HeadCell>
            <Table.HeadCell className="text-center">Share</Table.HeadCell>
          </Table.Head>
          <Table.Body>
            <Table.Row>
              <Table.Cell>
                <Checkbox />
              </Table.Cell>
              <Table.Cell>test.pdf</Table.Cell>
              <Table.Cell>12/12/2024</Table.Cell>
              <Table.Cell className="flex justify-center text-center">
                <Button outline color="purple">
                  <FaShare className="h-4 w-4" />
                </Button>
              </Table.Cell>
            </Table.Row>
          </Table.Body>
        </Table>
      </Card>
    </Modal.Body>
  );
};
