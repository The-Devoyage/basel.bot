import { Typography } from "@/shared/typography";
import { Avatar, Card, ListGroup, ListGroupItem } from "flowbite-react";
import Image from "next/image";

export const Members = () => {
  const members = [
    { full_name: "nick mclean", uuid: "12345" },
    { full_name: "Oakley McLean", uuid: "132049" },
  ];

  return (
    <Card>
      <Typography.Heading className="text-xl">Members</Typography.Heading>
      <ListGroup className="flex flex-col gap-2">
        {members.map((m) => (
          <ListGroupItem key={m.uuid}>
            <div className="flex items-center gap-2">
              <Avatar
                img={(props) => (
                  <Image
                    alt="user profile image"
                    src="https://avatar.iran.liara.run/public"
                    width={100}
                    height={100}
                    {...props}
                  />
                )}
              />
              <Typography.Heading className="font-bold">
                {m.full_name}
              </Typography.Heading>
              <Typography.Heading className="text-xs">admin</Typography.Heading>
            </div>
          </ListGroupItem>
        ))}
      </ListGroup>
    </Card>
  );
};
