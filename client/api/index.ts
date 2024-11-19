import { ShareableLink } from "@/types/shareable-link";
import { Subscription } from "@/types/subscription";
import { User } from "@/types/user";

export * from "./callApi";

export interface Response<T> {
  success: boolean;
  data: T | null;
  message?: string;
  code?: number;
}

export enum Endpoint {
  ShareableLinks = "/shareable-links",
  CreateShareableLink = "/shareable-link",
  UpdateShareableLink = "/shareable-link/:uuid",
  Me = "/me",
  AuthFinish = "/auth-finish",
  Logout = "/logout",
  Verify = "/verify",
  SubscribeStart = "/subscribe-start",
  GetSubscriptions = "/subscriptions",
}

type ShareableLinksQuery = { limit?: number; offset?: number };

interface EndpointParams {
  [Endpoint.ShareableLinks]: {
    query: ShareableLinksQuery;
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
}

export interface EndpointResponse {
  [Endpoint.ShareableLinks]: ShareableLink[];
  [Endpoint.CreateShareableLink]: ShareableLink;
  [Endpoint.Me]: User;
  [Endpoint.Logout]: null;
  [Endpoint.Verify]: null;
  [Endpoint.AuthFinish]: null;
  [Endpoint.UpdateShareableLink]: ShareableLink;
  [Endpoint.SubscribeStart]: { url: string };
  [Endpoint.GetSubscriptions]: Subscription[];
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
