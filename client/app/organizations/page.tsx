import { PageHeader } from "@/shared/layout/page-header";
import {
  AddOrganizationButton,
  EditOrganizationModal,
  ListOrganizations,
} from "./components";
import { Alert } from "flowbite-react";
import { OrganizationsPageProvider } from "./context";

const Organizations = () => {
  return (
    <section className="container mx-auto flex w-full flex-col space-y-2 p-4">
      <OrganizationsPageProvider>
        <div className="flex items-center justify-between">
          <PageHeader title="My Organizations" />
          <AddOrganizationButton />
        </div>
        <Alert color="pink" className="border-2 border-pink-300">
          <h2 className="text-xl">Opportunities Come From Organizations</h2>
          <p>
            Connect with top talent or discover your next big opportunity.
            Organizations make it easy to participate in interviews tailored to
            your goals.
          </p>
        </Alert>
        <ListOrganizations />
        <EditOrganizationModal />
      </OrganizationsPageProvider>
    </section>
  );
};

export default Organizations;
