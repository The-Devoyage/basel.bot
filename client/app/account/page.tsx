import { PageHeader } from "@/shared/layout/page-header";
import { ManageSubscription, Profile } from "./components";

const AccountPage = () => {
  return (
    <section className="container mx-auto flex w-full flex-col p-4">
      <PageHeader title="Account" />
      <Profile />
      <ManageSubscription />
    </section>
  );
};

export default AccountPage;
