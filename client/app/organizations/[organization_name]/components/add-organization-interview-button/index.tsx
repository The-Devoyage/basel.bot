"use client";

import { useHandleMessage } from "@/app/components/init-screen/components";
import { Organization } from "@/types";
import { Button, Tooltip } from "flowbite-react";
import { FC } from "react";
import { BsPlusLg } from "react-icons/bs";

export const AddOrganizationInterviewButton: FC<{
  organization_uuid: Organization["uuid"];
}> = ({ organization_uuid }) => {
  const { handleMessage } = useHandleMessage();

  const handleClick = () => {
    handleMessage(
      "create_organization_interview",
      null,
      `Organization UUID: ${organization_uuid}`,
    );
  };

  return (
    <Tooltip content="Create New Interview">
      <Button gradientMonochrome="purple" outline onClick={handleClick}>
        <BsPlusLg className="h-4 w-4" />
      </Button>
    </Tooltip>
  );
};
