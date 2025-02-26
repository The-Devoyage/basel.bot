import { InterviewAssessment } from "@/types/interview_assessment";

export const SET_INTERVIEW_ASSESSMENT = "SET_INTERVIEW_ASSESSMENT";

export type SetInterviewAssessmentAction = {
  type: typeof SET_INTERVIEW_ASSESSMENT;
  payload: {
    interviewAssessment: InterviewAssessment;
  };
};

export type Action = SetInterviewAssessmentAction;
export type State = {
  interviewAssessment: { assessment: InterviewAssessment | null };
};

export const interviewAssessmentReducer = (
  state: State,
  action: Action,
): State => {
  switch (action.type) {
    case SET_INTERVIEW_ASSESSMENT:
      return {
        ...state,
        interviewAssessment: {
          assessment: action.payload.interviewAssessment,
        },
      };
    default:
      return state;
  }
};

export const SetInterviewAssessment = (
  interviewAssessment: InterviewAssessment,
): SetInterviewAssessmentAction => ({
  type: SET_INTERVIEW_ASSESSMENT,
  payload: {
    interviewAssessment,
  },
});
