import { Endpoint, callApi } from "@/api";
import { Typography } from "@/shared/typography";
import { Alert, Badge, Card } from "flowbite-react";
import { SubscribeButton } from "./components";
import { FaApplePay, FaGooglePay } from "react-icons/fa";
import { CiCreditCard1 } from "react-icons/ci";

export const ManageSubscription = async () => {
  const subscriptionRes = await callApi({
    endpoint: Endpoint.GetSubscription,
    path: null,
    body: null,
    query: null,
  });
  const subscription = subscriptionRes.data;

  const getSubscriptionStatus = () => {
    if (subscription?.subscription_status.is_free_trial) {
      return {
        key: "FREE_TRIAL",
        badgeColor: "cyan",
        label: "Free Trial",
      };
    }
    if (subscription?.subscription_status.active) {
      return {
        key: "ACTIVE",
        badgeColor: "success",
        label: "Active",
      };
    } else {
      return {
        key: "INACTIVE",
        badgeColor: "failure",
        label: "Inactive",
      };
    }
  };

  return (
    <Card
      style={{
        boxShadow: "-11px 0 10px RGBA(118, 169, 250, 0.2)",
        borderLeft: "4px solid #c026d3",
      }}
    >
      <div className="flex justify-between">
        <Typography.Heading className="mb-2 text-2xl">
          Subscription
        </Typography.Heading>
        <Badge color={getSubscriptionStatus().badgeColor}>
          {getSubscriptionStatus().label}
        </Badge>
      </div>
      <Alert color="light">
        <Typography.Heading className="text-lg">
          Your Subscription
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
      <span className="flex items-center justify-between">
        <div className="flex space-x-2">
          <FaApplePay className="text-4xl dark:text-white" />
          <FaGooglePay className="text-4xl dark:text-white" />
          <CiCreditCard1 className="text-4xl dark:text-white" />
        </div>
        <SubscribeButton hasSubscribed={!!subscription} />
      </span>
    </Card>
  );
};
