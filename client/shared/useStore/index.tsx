import { Reducer, useReducer } from "react";
import {
  Action as ToastAction,
  toastReducer,
  State as ToastState,
} from "./toast";
import { Action as AuthAction, authReducer, State as AuthState } from "./auth";

export type AppAction = ToastAction | AuthAction;
export type AppState = ToastState & AuthState;

export const useStore = () => {
  const store = useReducer<Reducer<AppState, AppAction>>(
    (state, action) => {
      const reducers = [toastReducer, authReducer];
      let updated = state;
      for (const reducer of reducers) {
        const newState = reducer(state, action as any);
        updated = { ...state, ...newState };
      }
      return updated;
    },
    {
      toasts: [],
      token: null,
    },
  );

  return store;
};
