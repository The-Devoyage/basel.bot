"use client";

import { Endpoint, Response } from "@/api";
import { useCallApi } from "@/shared/useCallApi";
import { SubscriptionFeature, UserMeta } from "@/types";
import { useCheckPerm } from "@/utils/useCheckPerm";
import { ToggleSwitch, Tooltip } from "flowbite-react";
import { FC } from "react";

interface StatusCellProps {
  userMeta: UserMeta;
  refetch: () => Promise<Response<UserMeta[]> | undefined>;
}

export const StatusCell: FC<StatusCellProps> = ({ userMeta, refetch }) => {
  const allowManage = useCheckPerm(SubscriptionFeature.MANAGE_MEMORIES);
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
    <Tooltip
      content={
        allowManage
          ? "Enable/Disable memory."
          : "Upgrade membership to manage memories!"
      }
    >
      <ToggleSwitch
        checked={userMeta.status}
        onChange={handleChange}
        color="green"
        disabled={!allowManage}
      />
    </Tooltip>
  );
};
