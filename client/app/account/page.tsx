import { PageHeader } from "@/shared/layout/page-header";
import { ManageSubscription } from "./components";

const AccountPage = () => {
  return (
    <section className="flex w-full flex-col">
      <PageHeader title="Account" />
      <ManageSubscription />
    </section>
  );
};

export default AccountPage;
