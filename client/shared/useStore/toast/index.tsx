import { Notification } from "@/shared/toaster";
import { Reducer } from "react";
import { v4 } from "uuid";

export const ADD_TOAST = "ADD_TOAST";
export const REMOVE_TOAST = "REMOVE_TOAST";

export type AddToastAction = {
  type: typeof ADD_TOAST;
  payload: {
    notification: Notification;
  };
};

export type RemoveToastAction = {
  type: typeof REMOVE_TOAST;
  payload: {
    notification: Notification;
  };
};

export type Action = AddToastAction | RemoveToastAction;
export type State = { toasts: Notification[] };

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

// Actions
export const addToast = (
  notification: Omit<Notification, "uuid">,
): AddToastAction => ({
  type: ADD_TOAST,
  payload: {
    notification: {
      ...notification,
      uuid: v4(),
    },
  },
});

export const removeToast = (notification: Notification): RemoveToastAction => ({
  type: REMOVE_TOAST,
  payload: { notification },
});
