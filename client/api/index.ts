import {
  User,
  UserMeta,
  ShareableLink,
  Subscription,
  Interview,
  Onboarding,
  Notification,
  File,
} from "@/types";
import { Standup } from "@/types/standup";

export * from "./callApi";

export interface Response<T> {
  success: boolean;
  data: T | null;
  message?: string;
  code?: number;
  total?: number;
}

export enum Endpoint {
  ShareableLink = "/shareable-link/:sl_token",
  ShareableLinks = "/shareable-links",
  CreateShareableLink = "/shareable-link",
  UpdateShareableLink = "/shareable-link/:uuid",
  Me = "/me",
  AuthFinish = "/auth-finish",
  Logout = "/logout",
  Verify = "/verify",
  SubscribeStart = "/subscribe-start",
  GetSubscriptions = "/subscriptions",
  ResetIndex = "/reset-index",
  GetUserMetas = "/user-metas",
  PatchUserMeta = "/user-meta/:uuid",
  GetInterviews = "/interviews",
  GetOnboarding = "/onboarding",
  GetStandups = "/standups",
  GetNotifications = "/notifications",
  GetSuggestion = "/suggest",
  GetFileUploadLink = "/file/upload-link",
  ActivateFile = "/file/activate",
  GetFiles = "/file/list",
  GetFileDownloadLink = "/file/download-link",
  UpdateUser = "/user/update",
}

type PaginationQuery = { limit?: number; offset?: number };

export interface EndpointParams {
  [Endpoint.ShareableLink]: {
    query: undefined;
    body: undefined;
    path: { sl_token: string };
  };
  [Endpoint.ShareableLinks]: {
    query: PaginationQuery;
    body: undefined;
    path: undefined;
  };
  [Endpoint.CreateShareableLink]: {
    query: undefined;
    body: undefined;
    path: undefined;
  };
  [Endpoint.UpdateShareableLink]: {
    query: undefined;
    body: { tag?: string; status?: boolean };
    path: { uuid: string };
  };
  [Endpoint.Me]: { query: undefined; body: undefined; path: undefined };
  [Endpoint.Logout]: { query: undefined; body: undefined; path: undefined };
  [Endpoint.Verify]: { query: undefined; body: undefined; path: undefined };
  [Endpoint.AuthFinish]: {
    query: undefined;
    body: { token: string };
    path: undefined;
  };
  [Endpoint.SubscribeStart]: {
    query: undefined;
    body: undefined;
    path: undefined;
  };
  [Endpoint.GetSubscriptions]: {
    query: undefined;
    body: undefined;
    path: undefined;
  };
  [Endpoint.ResetIndex]: {
    query: undefined;
    body: { chat_start_time?: string };
    path: undefined;
  };
  [Endpoint.GetUserMetas]: {
    query: PaginationQuery;
    body: undefined;
    path: undefined;
  };
  [Endpoint.PatchUserMeta]: {
    query: undefined;
    body: { status?: boolean; delete?: boolean };
    path: { uuid: string };
  };
  [Endpoint.GetInterviews]: {
    query: PaginationQuery & {
      created_by_me?: boolean;
      taken_by_me?: boolean;
    };
    body: undefined;
    path: undefined;
  };
  [Endpoint.GetOnboarding]: {
    query: undefined;
    body: undefined;
    path: undefined;
  };
  [Endpoint.GetStandups]: {
    query: PaginationQuery & {
      start_date?: Date;
      end_date?: Date;
    };
    body: undefined;
    path: undefined;
  };
  [Endpoint.GetNotifications]: {
    query: PaginationQuery & {
      read?: boolean;
    };
    body: undefined;
    path: undefined;
  };
  [Endpoint.GetSuggestion]: {
    query: undefined;
    body: undefined;
    path: undefined;
  };
  [Endpoint.GetFileUploadLink]: {
    query: {
      file_name: string;
      file_size: number;
      mimetype: string;
    };
    body: undefined;
    path: undefined;
  };
  [Endpoint.ActivateFile]: {
    query: undefined;
    body: { uuid: string };
    path: undefined;
  };
  [Endpoint.GetFiles]: {
    query: PaginationQuery;
    body: undefined;
    path: undefined;
  };
  [Endpoint.GetFileDownloadLink]: {
    query: { uuid: string };
    body: undefined;
    path: undefined;
  };
  [Endpoint.UpdateUser]: {
    query: undefined;
    body: {
      first_name?: string;
      last_name?: string;
      email?: string;
      profile_image?: File;
    };
    path: undefined;
  };
}

export interface EndpointResponse {
  [Endpoint.ShareableLink]: ShareableLink;
  [Endpoint.ShareableLinks]: ShareableLink[];
  [Endpoint.CreateShareableLink]: ShareableLink;
  [Endpoint.Me]: User;
  [Endpoint.Logout]: null;
  [Endpoint.Verify]: null;
  [Endpoint.AuthFinish]: { token: string };
  [Endpoint.UpdateShareableLink]: ShareableLink;
  [Endpoint.SubscribeStart]: { url: string };
  [Endpoint.GetSubscriptions]: Subscription[];
  [Endpoint.ResetIndex]: null;
  [Endpoint.GetUserMetas]: UserMeta[];
  [Endpoint.PatchUserMeta]: UserMeta;
  [Endpoint.GetInterviews]: Interview[];
  [Endpoint.GetOnboarding]: Onboarding;
  [Endpoint.GetStandups]: Standup[];
  [Endpoint.GetNotifications]: Notification[];
  [Endpoint.GetSuggestion]: { text: string };
  [Endpoint.GetFileUploadLink]: { upload_link: string; file_uuid: string };
  [Endpoint.ActivateFile]: File;
  [Endpoint.GetFiles]: File[];
  [Endpoint.GetFileDownloadLink]: { download_link: string };
  [Endpoint.UpdateUser]: User;
}

type QueryType<E extends Endpoint> = E extends keyof EndpointParams
  ? EndpointParams[E]["query"]
  : never;

type BodyType<E extends Endpoint> = E extends keyof EndpointParams
  ? EndpointParams[E]["body"]
  : never;

type PathType<E extends Endpoint> = E extends keyof EndpointParams
  ? EndpointParams[E]["path"]
  : never;

export interface ApiAction<E extends Endpoint> {
  endpoint: E;
  method?: "GET" | "POST" | "PATCH";
  query: QueryType<E> extends undefined ? null : QueryType<E>;
  body: BodyType<E> extends undefined ? null : BodyType<E>;
  path: PathType<E> extends undefined ? null : PathType<E>;
}
