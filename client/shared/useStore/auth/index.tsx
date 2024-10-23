import { Reducer } from "react";

export const ADD_TOKEN = "ADD_TOKEN";
export const REMOVE_TOKEN = "REMOVE_TOKEN";

export type AddTokenAction = {
  type: typeof ADD_TOKEN;
  payload: {
    token: string;
  };
};
export type RemoveTokenAction = {
  type: typeof REMOVE_TOKEN;
};

export type Action = AddTokenAction | RemoveTokenAction;
export type State = { token: string | null };

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
    default:
      return state;
  }
};

// Actions
export const addToken = (token: string): AddTokenAction => ({
  type: ADD_TOKEN,
  payload: { token },
});

export const removeToken = (): RemoveTokenAction => ({
  type: REMOVE_TOKEN,
});
