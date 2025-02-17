export enum SubscriptionTier {
  CANDIDATE = "candidate",
  CANDIDATE_PRO = "candidate_pro",
  ORGANIZATION = "organization",
}

export interface SubscriptionStatus {
  active: boolean;
  is_free_trial: boolean;
}

export interface Subscription {
  uuid: string;
  status: boolean;
  customer_id: string;
  subscription_status: SubscriptionStatus;
  file: number;
  tier: SubscriptionTier;
  created_at: string;
  updated_at: string;
  deleted_at: string;
}
