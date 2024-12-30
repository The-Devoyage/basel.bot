import {
  User,
  UserMeta,
  ShareableLink,
  Subscription,
  Interview,
  Onboarding,
  Notification,
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
}

type PaginationQuery = { limit?: number; offset?: number };

interface EndpointParams {
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
    body: { tag: string };
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
    body: { status?: boolean };
    path: { uuid: string };
  };
  [Endpoint.GetInterviews]: {
    query: PaginationQuery;
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
