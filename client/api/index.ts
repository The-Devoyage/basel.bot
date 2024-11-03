import { ShareableLink } from "@/types/shareable-link";
import { User } from "@/types/user";

export * from "./callApi";

export interface Response<T> {
  success: boolean;
  data: T | null;
}

export enum Endpoint {
  ShareableLinks = "/shareable-links",
  CreateShareableLink = "/shareable-link",
  Me = "/me",
  AuthFinish = "/auth-finish",
  Logout = "/logout",
  Verify = "/verify",
}

type ShareableLinksQuery = { limit?: number; offset?: number };

interface EndpointParams {
  [Endpoint.ShareableLinks]: { query: ShareableLinksQuery; body: undefined };
  [Endpoint.CreateShareableLink]: {
    query: undefined;
    body: { tag: string };
  };
  [Endpoint.Me]: { query: undefined; body: undefined };
  [Endpoint.Logout]: { query: undefined; body: undefined };
  [Endpoint.Verify]: { query: undefined; body: undefined };
  [Endpoint.AuthFinish]: { query: undefined; body: { token: string } };
}

export interface EndpointResponse {
  [Endpoint.ShareableLinks]: ShareableLink[];
  [Endpoint.CreateShareableLink]: ShareableLink;
  [Endpoint.Me]: User;
  [Endpoint.Logout]: null;
  [Endpoint.Verify]: null;
  [Endpoint.AuthFinish]: null;
}

type QueryType<E extends Endpoint> = E extends keyof EndpointParams
  ? EndpointParams[E]["query"]
  : never;

type BodyType<E extends Endpoint> = E extends keyof EndpointParams
  ? EndpointParams[E]["body"]
  : never;

export interface ApiAction<E extends Endpoint> {
  endpoint: E;
  method?: "GET" | "POST";
  query: QueryType<E> extends undefined ? null : QueryType<E>;
  body: BodyType<E> extends undefined ? null : Required<BodyType<E>>;
}
