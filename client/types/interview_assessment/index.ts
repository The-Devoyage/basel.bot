import { Interview, User } from "..";

export interface InterviewAssessment {
  uuid: string;
  user: User;
  interview: Interview;
  overall: number;
  content_relevance?: number;
  communication_skills?: number;
  confidence_delivery?: number;
  structure_organization?: number;
  adaptability_critical_thinking?: number;
  technical_industry_knowledge?: number;
}
