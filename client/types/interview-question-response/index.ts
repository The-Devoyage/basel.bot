import { User } from "..";
import { InterviewQuestion } from "../interview-question";

export interface InterviewQuestionResponse {
  user: User;
  interview_question: InterviewQuestion;
  response: string;
  status: boolean;
}
