"use client";

import { Button } from "flowbite-react";
import { useContext } from "react";
import { BsPlusLg } from "react-icons/bs";
import { OrganizationsPageContext } from "../../context";

export const AddOrganizationButton = () => {
  const { toggleEditOrganizationModal } = useContext(OrganizationsPageContext);

  return (
    <>
      <Button
        outline
        gradientMonochrome="pink"
        onClick={toggleEditOrganizationModal}
      >
        <BsPlusLg className="size-4" />
      </Button>
    </>
  );
};
