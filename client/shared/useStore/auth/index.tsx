import { User } from "@/types/user";
import { Reducer } from "react";

export const ADD_TOKEN = "ADD_TOKEN";
export const REMOVE_TOKEN = "REMOVE_TOKEN";
export const SET_ME = "SET_ME";

export type AddTokenAction = {
  type: "ADD_TOKEN";
  payload: {
    token: string;
  };
};
export type RemoveTokenAction = {
  type: "REMOVE_TOKEN";
};
export type SetMeAction = {
  type: "SET_ME";
  payload: {
    me: User | null;
  };
};

export type Action = AddTokenAction | RemoveTokenAction | SetMeAction;
export type State = { token: string | null; me: User | null };

export const setMe = (me: User | null): SetMeAction => ({
  type: SET_ME,
  payload: {
    me,
  },
});

export const authReducer: Reducer<State, Action> = (
  state: State,
  action: Action,
): State => {
  switch (action.type) {
    case ADD_TOKEN:
      return {
        ...state,
        token: action.payload.token,
      };
    case REMOVE_TOKEN:
      return {
        ...state,
        token: null,
      };
    case SET_ME:
      return {
        ...state,
        me: action.payload.me,
      };
    default:
      return state;
  }
};
