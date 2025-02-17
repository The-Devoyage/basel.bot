import { GlobalContext } from "@/app/provider";
import { SubscriptionFeature } from "@/types";
import { useContext } from "react";

export const useCheckPerm = (feature: SubscriptionFeature) => {
  const {
    store: {
      auth: { me },
    },
  } = useContext(GlobalContext);
  const allowManage = me?.subscription?.features.includes(feature);
  return allowManage;
};
