import { Typography } from "@/shared/typography";
import { OrganizationUser } from "@/types";
import { Avatar, Card } from "flowbite-react";
import { FC } from "react";

export const Members: FC<{ users: OrganizationUser[] }> = ({ users }) => (
  <Card>
    <Typography.Heading className="text-xl">Recruiters</Typography.Heading>
    <ul className="flex flex-col gap-2">
      {users.map((u) => (
        <li key={u.uuid} className="rounded border-2 px-4 py-2">
          <div className="flex items-center gap-2">
            <Avatar
              rounded
              img={u.user.profile_image?.url}
              placeholderInitials={u.user.first_initial}
              bordered
              color="success"
              theme={{
                root: {
                  img: {
                    on: "flex items-center justify-center object-cover",
                  },
                },
              }}
            />
            <Typography.Heading className="font-bold">
              {u.user.full_name}
            </Typography.Heading>
            <Typography.Heading className="text-xs">admin</Typography.Heading>
          </div>
        </li>
      ))}
    </ul>
  </Card>
);
