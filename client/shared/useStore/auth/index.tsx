import { ShareableLink } from "@/types";
import { User } from "@/types/user";

export const SET_AUTHENTICATED = "SET_AUTHENTICATED";
export const SET_ME = "SET_ME";
export const SET_SHAREABLE_LINK = "SET_SHAREABLE_LINK";

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
export type SetShareableLinkAction = {
  type: typeof SET_SHAREABLE_LINK;
  payload: {
    shareableLink: ShareableLink;
  };
};

export type Action =
  | SetAuthenticatedAction
  | SetMeAction
  | SetShareableLinkAction;
export type State = {
  auth: {
    isAuthenticated: boolean | null;
    me: User | null;
    shareableLink: ShareableLink | null;
  };
};

export const authReducer = (state: State, action: Action): State => {
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
    case SET_SHAREABLE_LINK:
      return {
        ...state,
        auth: { ...state.auth, shareableLink: action.payload.shareableLink },
      };
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

export const setShareableLink = (
  shareableLink: ShareableLink,
): SetShareableLinkAction => ({
  type: SET_SHAREABLE_LINK,
  payload: { shareableLink },
});
