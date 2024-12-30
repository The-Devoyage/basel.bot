import { Reducer, useReducer } from "react";
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

export type AppAction = ToastAction | AuthAction | NotificationAction;
export type AppState = ToastState & AuthState & NotificationState;
export type AppStore = [AppState, React.Dispatch<AppAction>];

export const useStore = () => {
  const store = useReducer<Reducer<AppState, AppAction>>(
    (state, action) => {
      const reducers = [toastReducer, authReducer, notificationReducer];
      let updated = { ...state };
      for (const reducer of reducers) {
        const newState = reducer(updated, action as any);
        updated = { ...updated, ...newState };
      }
      return updated;
    },
    {
      toasts: [],
      isAuthenticated: false,
      me: null,
      notifications: { open: false },
    },
  );

  return store;
};
