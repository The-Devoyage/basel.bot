export enum SubscriptionTier {
  CANDIDATE = "candidate",
  CANDIDATE_PRO = "candidate_pro",
  ORGANIZATION = "organization",
}

export interface SubscriptionStatus {
  active: boolean;
  is_free_trial: boolean;
}

export enum SubscriptionFeature {
  CREATE_INTERVIEW = "create_interview",
  UNLIMITED_MEMORIES = "unlimited_metas",
  MANAGE_MEMORIES = "manage_memories",
  MANAGE_ORGANIZATION = "manage_organization",
}

export interface Subscription {
  uuid: string;
  status: boolean;
  customer_id: string;
  subscription_status: SubscriptionStatus;
  features: SubscriptionFeature[];
  file: number;
  tier: SubscriptionTier;
  created_at: string;
  updated_at: string;
  deleted_at: string;
}
