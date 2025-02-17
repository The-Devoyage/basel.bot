import { Typography } from "@/shared/typography";
import { Card } from "flowbite-react";
import { CheckoutButton } from "./components";

const SubscribePage = () => {
  return (
    <section className="container mx-auto flex w-full flex-col items-center justify-center space-y-4 p-4">
      <Card>
        <Typography.Heading>You&apos;re on the way...</Typography.Heading>
        <Typography.Paragraph>
          Redirecting to secure checkout.
        </Typography.Paragraph>
        <CheckoutButton />
      </Card>
    </section>
  );
};

export default SubscribePage;
