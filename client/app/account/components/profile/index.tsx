"use client";

import { GlobalContext } from "@/app/provider";
import { FileManager } from "@/shared/file-manager";
import { Typography } from "@/shared/typography";
import { Avatar, Button, Card, Label, TextInput } from "flowbite-react";
import { useContext, useState } from "react";

export const Profile = () => {
  const {
    store: { me },
  } = useContext(GlobalContext);
  const [showFileManager, setShowFileManager] = useState(false);

  return (
    <Card
      className="mb-4"
      style={{
        boxShadow: "-11px 0 10px RGBA(118, 169, 250, 0.2)",
        borderLeft: "4px solid #10B981",
      }}
    >
      <FileManager
        show={showFileManager}
        onClose={() => setShowFileManager(false)}
      />
      <div className="flex justify-between">
        <Typography.Heading className="mb-2 text-2xl">
          Profile
        </Typography.Heading>
      </div>
      <div className="flex w-full flex-col items-center justify-center space-y-4 text-4xl">
        <Avatar
          bordered
          size="xl"
          rounded
          placeholderInitials={me?.full_name?.at(0) || me?.email.at(0)}
          color="success"
        />
        <Button color="green" outline onClick={() => setShowFileManager(true)}>
          Update Profile Image
        </Button>
      </div>
      <Label>Email</Label>
      <TextInput placeholder="email" value={me?.email} readOnly />
      <Label>First Name</Label>
      <TextInput placeholder="Jane" value={me?.first_name} />
      <Label>Last Name</Label>
      <TextInput placeholder="Doe" value={me?.last_name} />
      <div className="flex justify-end">
        <Button color="green" outline>
          Save
        </Button>
      </div>
    </Card>
  );
};
