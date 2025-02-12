"use client";

import { useHandleMessage } from "@/app/components/init-screen/components";
import { GlobalContext } from "@/app/provider";
import { Organization } from "@/types";
import { Button, Tooltip } from "flowbite-react";
import { FC, useContext } from "react";
import { BsPlusLg } from "react-icons/bs";

export const AddOrganizationInterviewButton: FC<{
  organization_uuid: Organization["uuid"];
  members: Organization["users"];
}> = ({ organization_uuid, members }) => {
  const { handleMessage } = useHandleMessage();
  const {
    store: {
      auth: { me },
    },
  } = useContext(GlobalContext);

  const handleClick = () => {
    handleMessage(
      "create_organization_interview",
      null,
      `Organization UUID: ${organization_uuid}`,
    );
  };

  if (members.findIndex((m) => m.user.uuid === me?.uuid) === -1) {
    return null;
  }

  return (
    <Tooltip content="Create New Interview">
      <Button gradientMonochrome="purple" outline onClick={handleClick}>
        <BsPlusLg className="h-4 w-4" />
      </Button>
    </Tooltip>
  );
};
