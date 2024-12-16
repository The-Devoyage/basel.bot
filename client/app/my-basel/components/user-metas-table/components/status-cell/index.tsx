"use client";

import { Endpoint, Response } from "@/api";
import { useCallApi } from "@/shared/useCallApi";
import { UserMeta } from "@/types";
import { ToggleSwitch } from "flowbite-react";
import { FC } from "react";

interface StatusCellProps {
  userMeta: UserMeta;
  refetch: () => Promise<Response<UserMeta[]> | undefined>;
}

export const StatusCell: FC<StatusCellProps> = ({ userMeta, refetch }) => {
  const { call } = useCallApi(
    {
      endpoint: Endpoint.PatchUserMeta,
      method: "PATCH",
      path: {
        uuid: userMeta.uuid,
      },
      body: {
        status: !userMeta.status,
      },
      query: null,
    },
    {
      toast: {
        onSuccess: true,
      },
      successMessage:
        "Updated Memory Index. Re-Train Basel in order to sync the memory.",
      onSuccess: () => {
        refetch();
      },
    },
  );

  const handleChange = async () => {
    await call();
  };

  return (
    <ToggleSwitch
      checked={userMeta.status}
      onChange={handleChange}
      color="green"
    />
  );
};
