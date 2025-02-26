import { useReducer } from "react";
import {
  Action as ToastAction,
  toastReducer,
  State as ToastState,
} from "./toast";
import { Action as AuthAction, authReducer, State as AuthState } from "./auth";
import {
  Action as NotificationAction,
  State as NotificationState,
  notificationReducer,
} from "./notification";
import {
  Action as ChatInputAction,
  State as ChatInputState,
  chatInputReducer,
} from "./chatInput";
import {
  Action as InterviewAssessmentAction,
  State as InterviewAssessmentState,
  interviewAssessmentReducer,
} from "./interviewAssessment";

export type AppAction =
  | ToastAction
  | AuthAction
  | NotificationAction
  | ChatInputAction
  | InterviewAssessmentAction;

export type AppState = ToastState &
  AuthState &
  NotificationState &
  ChatInputState &
  InterviewAssessmentState;
export type AppStore = [AppState, React.Dispatch<AppAction>];

export const useStore = () => {
  const store = useReducer<AppState, [AppAction]>(
    (state, action) => {
      const reducers = [
        toastReducer,
        authReducer,
        notificationReducer,
        chatInputReducer,
        interviewAssessmentReducer,
      ];
      let updated = { ...state };
      for (const reducer of reducers) {
        const newState = reducer(updated, action as any);
        updated = { ...updated, ...newState };
      }
      return updated;
    },
    {
      toasts: [],
      auth: {
        isAuthenticated: false,
        me: null,
        shareableLink: null,
      },
      notifications: { open: false },
      chatInput: { focused: false },
      interviewAssessment: { assessment: null },
    },
  );

  return store;
};
