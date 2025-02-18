"use client";

import { Endpoint, Response } from "@/api";
import { useCallApi } from "@/shared/useCallApi";
import { SubscriptionFeature, UserMeta } from "@/types";
import { useCheckPerm } from "@/utils/useCheckPerm";
import { Button, Tooltip } from "flowbite-react";
import { FC } from "react";
import { MdDeleteSweep } from "react-icons/md";

interface DeleteCellProps {
  userMeta: UserMeta;
  refetch: () => Promise<Response<UserMeta[]> | undefined>;
}

export const DeleteCell: FC<DeleteCellProps> = ({ userMeta, refetch }) => {
  const allowManage = useCheckPerm(SubscriptionFeature.MANAGE_MEMORIES);
  const { call, loading } = useCallApi(
    {
      endpoint: Endpoint.PatchUserMeta,
      method: "PATCH",
      path: {
        uuid: userMeta.uuid,
      },
      body: {
        delete: true,
      },
      query: null,
    },
    {
      toast: {
        onSuccess: true,
      },
      successMessage: "Deleted Memory.",
      onSuccess: () => {
        refetch();
      },
    },
  );

  const handleClick = async () => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this memory?",
    );
    if (confirmed) await call();
  };
  return (
    <Tooltip
      content={
        allowManage
          ? "Delete Memory?"
          : "Upgrade membership to delete memories!"
      }
    >
      <Button
        color="failure"
        outline
        onClick={handleClick}
        isProcessing={loading}
        disabled={!allowManage}
      >
        <MdDeleteSweep />
      </Button>
    </Tooltip>
  );
};
