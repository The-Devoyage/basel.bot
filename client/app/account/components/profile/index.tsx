import { Endpoint, callApi } from "@/api";
import { Card } from "flowbite-react";
import { UpdateUserForm } from "./components";

export const Profile = async () => {
  const me = await callApi({
    endpoint: Endpoint.Me,
    query: null,
    body: null,
    path: null,
  });

  return (
    <Card
      className="mb-4"
      style={{
        boxShadow: "-11px 0 10px RGBA(118, 169, 250, 0.2)",
        borderLeft: "4px solid #10B981",
      }}
    >
      <UpdateUserForm me={me.data} />
    </Card>
  );
};
