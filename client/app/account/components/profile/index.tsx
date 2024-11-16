"use client";
import { GlobalContext } from "@/app/provider";
import { Typography } from "@/shared/typography";
import { Card, Label, TextInput } from "flowbite-react";
import { useContext } from "react";

export const Profile = () => {
  const {
    store: { me },
  } = useContext(GlobalContext);

  return (
    <Card className="mb-4">
      <div className="flex justify-between">
        <Typography.Heading className="mb-2 text-2xl">
          Profile
        </Typography.Heading>
        {/* <Button size="sm" color="green" outline> */}
        {/*   Save */}
        {/* </Button> */}
      </div>
      <Label>Email</Label>
      <TextInput placeholder="email" value={me?.email} readOnly />
      {/* <Label>First Name</Label> */}
      {/* <TextInput placeholder="Jane" /> */}
      {/* <Label>Last Name</Label> */}
      {/* <TextInput placeholder="Doe" /> */}
    </Card>
  );
};
