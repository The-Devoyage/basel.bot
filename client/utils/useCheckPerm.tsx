import { GlobalContext } from "@/app/provider";
import { SubscriptionFeature } from "@/types";
import { useContext } from "react";

export const useCheckPerm = (feature: SubscriptionFeature) => {
  const {
    store: {
      auth: { me },
    },
  } = useContext(GlobalContext);
  if (me?.subscription_status.is_free_trial) return true;
  const allowManage =
    me?.subscription_status.subscription?.features.includes(feature);
  return allowManage;
};
