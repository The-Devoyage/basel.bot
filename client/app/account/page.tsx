import { PageHeader } from "@/shared/layout/page-header";
import { Typography } from "@/shared/typography";
import { Badge, Card } from "flowbite-react";
import { Profile } from "./components";

const AccountPage = () => {
  return (
    <section className="flex w-full flex-col">
      <PageHeader title="Account" />
      <Profile />
      <Card>
        <div className="flex justify-between">
          <Typography.Heading className="mb-2 text-2xl">
            Subscription
          </Typography.Heading>
          <Badge color="success">Active $3.99/mo</Badge>
        </div>
        <span className="flex">
          <Typography.Paragraph className="mr-3">
            Manage your subscription through the
          </Typography.Paragraph>
          <Typography.Link
            href={process.env.NEXT_PUBLIC_BILLING_PORTAL_URL}
            className="underline"
          >
            Billing Portal.
          </Typography.Link>
        </span>
      </Card>
    </section>
  );
};

export default AccountPage;
