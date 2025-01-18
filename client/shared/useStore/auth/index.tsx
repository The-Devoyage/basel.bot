import { User } from "@/types/user";
import { Reducer } from "react";

export const SET_AUTHENTICATED = "SET_AUTHENTICATED";
export const SET_ME = "SET_ME";

export type SetAuthenticatedAction = {
  type: typeof SET_AUTHENTICATED;
  payload: {
    isAuthenticated: boolean | null;
  };
};
export type SetMeAction = {
  type: typeof SET_ME;
  payload: {
    me: User;
  };
};

export type Action = SetAuthenticatedAction | SetMeAction;
export type State = {
  auth: { isAuthenticated: boolean | null; me: User | null };
};

export const authReducer: Reducer<State, Action> = (
  state: State,
  action: Action,
): State => {
  switch (action.type) {
    case SET_AUTHENTICATED:
      return {
        ...state,
        auth: {
          ...state.auth,
          isAuthenticated: action.payload.isAuthenticated,
        },
      };
    case SET_ME:
      return { ...state, auth: { ...state.auth, me: action.payload.me } };
    default:
      return { ...state };
  }
};

// Actions
export const setAuthenticated = (
  isAuthenticated: boolean | null,
): SetAuthenticatedAction => ({
  type: SET_AUTHENTICATED,
  payload: { isAuthenticated },
});

export const setMe = (me: User): SetMeAction => ({
  type: SET_ME,
  payload: { me },
});
