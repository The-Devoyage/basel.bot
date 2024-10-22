import { Notification } from "@/shared/toaster";
import { Reducer } from "react";

export type Action = {
  type: "ADD_TOAST" | "REMOVE_TOAST";
  payload: {
    notification: Notification;
  };
};

export type State = { toasts: Notification[] };

export const ADD_TOAST = "ADD_TOAST";
export const REMOVE_TOAST = "REMOVE_TOAST";

export const toastReducer: Reducer<State, Action> = (
  state: State,
  action: Action,
): State => {
  switch (action.type) {
    case ADD_TOAST:
      return {
        toasts: [...state.toasts, action.payload.notification],
      };
    case REMOVE_TOAST:
      return {
        toasts: state.toasts.filter(
          (toast) => toast.uuid !== action.payload.notification.uuid,
        ),
      };
    default:
      return state;
  }
};
