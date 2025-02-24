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
  organization?: Organization;
  description: string;
  question_count: number;
  response_count: number;
  total_response_count: number;
  submitted: boolean;
  status: boolean;
  created_at: string;
  updated_at: string;
  deleted_at: string;
}
