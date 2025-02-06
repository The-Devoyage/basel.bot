import { PageHeader } from "@/shared/layout/page-header";
import { AddOrganizationButton, ListOrganizations } from "./components";
import { Alert } from "flowbite-react";
import { OrganizationsPageProvider } from "./context";

const Organizations = () => {
  return (
    <section className="container mx-auto flex w-full flex-col space-y-2 p-4">
      <OrganizationsPageProvider>
        <div className="flex items-center justify-between">
          <PageHeader title="Organizations" />
          <AddOrganizationButton />
        </div>
        <Alert color="pink" className="border-2 border-pink-300">
          <h2 className="text-xl">Recruit with Basel</h2>
          <p>Interviews</p>
        </Alert>
        <ListOrganizations />
      </OrganizationsPageProvider>
    </section>
  );
};

export default Organizations;
