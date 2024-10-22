import { Reducer } from "react";

export type AddTokenAction = {
  type: "ADD_TOKEN";
  payload: {
    token: string;
  };
};

export type RemoveTokenAction = {
  type: "REMOVE_TOKEN";
};

export type Action = AddTokenAction | RemoveTokenAction;

export type State = { token: string | null };

export const ADD_TOKEN = "ADD_TOKEN";
export const REMOVE_TOKEN = "REMOVE_TOKEN";

export const authReducer: Reducer<State, Action> = (
  state: State,
  action: Action,
): State => {
  switch (action.type) {
    case ADD_TOKEN:
      return {
        token: action.payload.token,
      };
    case REMOVE_TOKEN:
      return {
        token: null,
      };
    default:
      return state;
  }
};
