import { Reducer } from "react";

export const TOGGLE_NOTIFICATION_DRAWER = "TOGGLE_NOTIFICATION_DRAWER";

export type ToggleNotificationDrawerAction = {
  type: typeof TOGGLE_NOTIFICATION_DRAWER;
  payload: {
    open: boolean;
  };
};

export type Action = ToggleNotificationDrawerAction;
export type State = { notifications: { open: boolean } };

export const notificationReducer: Reducer<State, Action> = (
  state: State,
  action: Action,
): State => {
  switch (action.type) {
    case TOGGLE_NOTIFICATION_DRAWER:
      return {
        ...state,
        notifications: {
          open: action.payload.open,
        },
      };
    default:
      return state;
  }
};

// Actions
export const toggleNotificationDrawer = (
  open: boolean,
): ToggleNotificationDrawerAction => ({
  type: TOGGLE_NOTIFICATION_DRAWER,
  payload: {
    open,
  },
});
