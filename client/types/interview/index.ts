import { Organization } from "..";

export enum InterviewType {
  GENERAL = "general",
  APPLICATION = "application",
}

export interface Interview {
  uuid: string;
  interview_type: InterviewType;
  position: string;
  url?: string;
  organization?: Pick<Organization, "uuid" | "name" | "slug">;
  description: string;
  question_count: number;
  response_count: number;
  status: boolean;
  created_at: string;
  updated_at: string;
  deleted_at: string;
}
