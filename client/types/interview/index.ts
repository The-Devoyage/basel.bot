export enum InterviewType {
  GENERAL = "general",
  APPLICATION = "application",
}

export interface Interview {
  uuid: string;
  name: string;
  interview_type: InterviewType;
  url?: string;
  organization_name?: string;
  position?: string;
  description: string;
  question_count: number;
  response_count: number;
  status: boolean;
  created_at: string;
  updated_at: string;
  deleted_at: string;
}
