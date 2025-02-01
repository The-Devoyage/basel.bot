import { Reducer } from "react";

export const TOGGLE_FOCUS_CHAT_INPUT = "TOGGLE_FOCUS_CHAT_INPUT";

export type ToggleFocusChatInputAction = {
  type: typeof TOGGLE_FOCUS_CHAT_INPUT;
  payload: {
    focused: boolean;
  };
};

export type Action = ToggleFocusChatInputAction;
export type State = { chatInput: { focused: boolean } };

export const chatInputReducer: Reducer<State, Action> = (
  state,
  action,
): State => {
  switch (action.type) {
    case TOGGLE_FOCUS_CHAT_INPUT:
      return {
        ...state,
        chatInput: {
          focused: action.payload.focused,
        },
      };
    default:
      return state;
  }
};

export const toggleChatInputFocus = (
  focused: boolean,
): ToggleFocusChatInputAction => ({
  type: TOGGLE_FOCUS_CHAT_INPUT,
  payload: {
    focused,
  },
});
