"use client";

import { Endpoint } from "@/api";
import { FileManager } from "@/shared/file-manager";
import { Typography } from "@/shared/typography";
import { useCallApi } from "@/shared/useCallApi";
import { User, ValidMimeType } from "@/types";
import { Avatar, Button, Label, TextInput } from "flowbite-react";
import { FC, FormEvent, useEffect, useState } from "react";
import { File } from "@/types";

interface UpdateUserForm {
  first_name?: string;
  last_name?: string;
  email?: string;
  profile_image?: File;
}

export const UpdateUserForm: FC<{ me: User | null }> = ({ me }) => {
  const [form, setForm] = useState<UpdateUserForm>({
    first_name: "",
    last_name: "",
    email: "",
    profile_image: undefined,
  });
  const [showFileManager, setShowFileManager] = useState(false);
  const updateUser = useCallApi(
    {
      endpoint: Endpoint.UpdateUser,
      method: "PATCH",
      body: {},
      query: null,
      path: null,
    },
    {
      toast: {
        onSuccess: true,
      },
      successMessage: "User updated.",
      callApiOptions: {
        revalidationTag: "me",
      },
    },
  );

  useEffect(() => {
    setForm({
      first_name: me?.first_name || "",
      last_name: me?.last_name || "",
      email: me?.email || "",
      profile_image: me?.profile_image,
    });
  }, [me]);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    await updateUser.call({
      body: { ...form, profile_image: form.profile_image?.uuid },
      query: null,
      path: null,
    });
  };
  return (
    <form onSubmit={handleSubmit}>
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
          placeholderInitials={
            form?.first_name?.at(0) ||
            form?.email?.at(0) ||
            me?.full_name?.at(0) ||
            me?.email.at(0)
          }
          color="success"
          img={form?.profile_image?.url}
          theme={{
            root: {
              img: {
                on: "flex items-center justify-center object-cover",
              },
            },
          }}
        />
        <FileManager
          show={showFileManager}
          onClose={() => setShowFileManager(false)}
          onSelect={(files) =>
            setForm({ ...form, profile_image: files?.at(0) })
          }
          validMimeTypes={[
            ValidMimeType.PNG,
            ValidMimeType.JPG,
            ValidMimeType.JPEG,
          ]}
        />
        <Button color="green" outline onClick={() => setShowFileManager(true)}>
          Update Profile Image
        </Button>
      </div>
      <Label>Email</Label>
      <TextInput
        placeholder="email"
        value={form.email}
        onChange={(e) => setForm({ ...form, email: e.currentTarget.value })}
      />
      <Label>First Name</Label>
      <TextInput
        placeholder="Jane"
        value={form.first_name}
        onChange={(e) =>
          setForm({ ...form, first_name: e.currentTarget.value })
        }
      />
      <Label>Last Name</Label>
      <TextInput
        placeholder="Doe"
        value={form.last_name}
        onChange={(e) => setForm({ ...form, last_name: e.currentTarget.value })}
      />
      <div className="mt-2 flex justify-end">
        <Button
          color="green"
          outline
          type="submit"
          isProcessing={updateUser.loading}
        >
          Save
        </Button>
      </div>
    </form>
  );
};
