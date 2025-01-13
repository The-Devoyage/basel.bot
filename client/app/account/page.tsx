import { PageHeader } from "@/shared/layout/page-header";
import { ManageSubscription, Profile } from "./components";

const AccountPage = () => {
  return (
    <section className="flex w-full flex-col">
      <PageHeader title="Account" />
      <Profile />
      <ManageSubscription />
    </section>
  );
};

export default AccountPage;
