export enum SubscriptionTier {
  CANDIDATE = "candidate",
  CANDIDATE_PRO = "candidate_pro",
  ORGANIZATION = "organization",
}

export interface SubscriptionStatus {
  active: boolean;
  is_free_trial: boolean;
  subscription?: Subscription;
  free_trial_expires?: Date;
}

export enum SubscriptionFeature {
  CREATE_INTERVIEW = "create_interview",
  LOG_STANDUP = "log_standup",
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
