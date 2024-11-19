import { Endpoint, callApi } from "@/api";
import { Typography } from "@/shared/typography";
import { Alert, Badge, Card } from "flowbite-react";
import { SubscribeButton } from "./components";
import { FaApplePay, FaGooglePay } from "react-icons/fa";
import { CiCreditCard1 } from "react-icons/ci";

export const ManageSubscription = async () => {
  const res = await callApi({
    endpoint: Endpoint.GetSubscriptions,
    path: null,
    body: null,
    query: null,
  });
  const hasSubscribed = !!res?.data?.length;

  return (
    <Card>
      <div className="flex justify-between">
        <Typography.Heading className="mb-2 text-2xl">
          Subscription
        </Typography.Heading>
        <Badge color={res?.data?.length ? "success" : "warning"}>
          {hasSubscribed ? "Active" : "Inactive"}
        </Badge>
      </div>
      <Alert>
        <Typography.Heading className="text-lg dark:!text-slate-900">
          Subscribing and Supporting
        </Typography.Heading>
        <ul role="list" className="list-inside list-disc">
          <li>
            <strong>Free 30 Day Trial</strong> - No pre-purchase required!
          </li>
          <li>
            <strong>Conversation Summaries</strong> - Basel remembers your
            conversations and can provide summaries for recruiters and potential
            employers.
          </li>
          <li>
            <strong>Chat History</strong> - Basel saves your chat history.
          </li>
        </ul>
      </Alert>
      {hasSubscribed ? (
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
      ) : (
        <span className="flex items-center justify-between">
          <div className="flex space-x-2">
            <FaApplePay className="text-4xl dark:text-white" />
            <FaGooglePay className="text-4xl dark:text-white" />
            <CiCreditCard1 className="text-4xl dark:text-white" />
          </div>
          <SubscribeButton />
        </span>
      )}
    </Card>
  );
};
