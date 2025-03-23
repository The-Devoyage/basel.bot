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
  total_assessments: number;
  started: boolean;
  submitted: boolean;
  status: boolean;
  created_at: string;
  updated_at: string;
  deleted_at: string;
}
