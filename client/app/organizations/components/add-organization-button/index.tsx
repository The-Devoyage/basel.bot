"use client";

import { Button, Tooltip } from "flowbite-react";
import { useContext } from "react";
import { BsPlusLg } from "react-icons/bs";
import { OrganizationsPageContext } from "../../context";
import { SubscriptionFeature } from "@/types";
import { useCheckPerm } from "@/utils/useCheckPerm";

export const AddOrganizationButton = () => {
  const { toggleEditOrganizationModal } = useContext(OrganizationsPageContext);
  const allowManage = useCheckPerm(SubscriptionFeature.MANAGE_ORGANIZATION);

  return (
    <Tooltip
      content={
        allowManage ? "Add Organization" : "Upgrade to create organizations!"
      }
      placement="bottom"
    >
      <Button
        outline
        gradientMonochrome="pink"
        onClick={toggleEditOrganizationModal}
        disabled={!allowManage}
      >
        <BsPlusLg className="size-4" />
      </Button>
    </Tooltip>
  );
};
