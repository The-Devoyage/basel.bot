import { Button } from "flowbite-react";
import { BsPlusLg } from "react-icons/bs";

export const AddOrganizationButton = () => {
  return (
    <>
      <Button outline gradientMonochrome="pink">
        <BsPlusLg className="h-4 w-4" />
      </Button>
    </>
  );
};
