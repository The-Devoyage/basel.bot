"use client";

import { User } from "@/types";
import { Avatar } from "flowbite-react";
import { FC } from "react";

export const UserAvatar: FC<{ chattingWith: User | null }> = ({
  chattingWith,
}) => {
  return (
    <Avatar
      alt="User Avatar"
      size="lg"
      rounded
      placeholderInitials={chattingWith?.first_initial}
      bordered
      color="success"
      img={chattingWith?.profile_image?.url}
      theme={{
        root: {
          img: {
            on: "flex items-center justify-center object-cover",
            placeholder: "absolute -bottom-2 h-auto w-auto text-gray-400",
          },
        },
      }}
    />
  );
};
