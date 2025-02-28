import {
  User,
  UserMeta,
  ShareableLink,
  Interview,
  Onboarding,
  Notification,
  File,
  ValidMimeType,
  Organization,
  SubscriptionTier,
  SubscriptionStatus,
  Message,
} from "@/types";
import { InterviewQuestion } from "@/types/interview-question";
import { InterviewAssessment } from "@/types/interview_assessment";
import { Standup } from "@/types/standup";

export * from "./callApi";

export interface Response<T> {
  success: boolean;
  data: T | null;
  message?: string;
  code?: number;
  total?: number;
  detail?: string;
  error?: string;
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
  GetSubscriptionStatus = "/subscription-status",
  ResetIndex = "/reset-index",
  GetUserMetas = "/user-metas",
  PatchUserMeta = "/user-meta/:uuid",
  GetInterviews = "/interview/list",
  GetInterview = "/interview",
  GetOnboarding = "/onboarding",
  GetStandups = "/standups",
  GetNotifications = "/notifications",
  GetSuggestion = "/suggest",
  GetFileUploadLink = "/file/upload-link",
  ActivateFile = "/file/activate",
  GetFiles = "/file/list",
  GetFileDownloadLink = "/file/download-link",
  UpdateUser = "/user/update",
  CreateOrganization = "/organization/create",
  GetOrganizations = "/organization/list",
  GetOrganization = "/organization",
  UpdateOrganization = "/organization/update",
  GetInterviewQuestions = "/interview-question/list",
  GetInterviewAssessments = "/interview-assessment/list",
  GetInterviewAssessment = "/interview-assessment",
  GetMessages = "/message/list",
}

type PaginationQuery = { limit?: number; offset?: number };

export interface EndpointParams {
  [Endpoint.ShareableLink]: {
    query: undefined;
    body: undefined;
    path: { sl_token: string };
  };
  [Endpoint.ShareableLinks]: {
    query: PaginationQuery & { interview_uuid?: string };
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
    body: { tag?: string; status?: boolean; interview_uuids?: string[] };
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
    query: { tier: SubscriptionTier };
    body: undefined;
    path: undefined;
  };
  [Endpoint.GetSubscriptionStatus]: {
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
      taken_by_me?: boolean;
      search_term?: string;
      sl_token?: string;
      organization_uuid?: string;
    };
    body: undefined;
    path: undefined;
  };
  [Endpoint.GetInterview]: {
    query: { uuid: string };
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
      sl_token?: string;
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
    query: PaginationQuery & { file_types?: ValidMimeType[] };
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
      profile_image?: File["uuid"];
    };
    path: undefined;
  };
  [Endpoint.CreateOrganization]: {
    query: undefined;
    body: {
      name: string;
      description: string;
      logo?: File;
    };
    path: undefined;
  };
  [Endpoint.UpdateOrganization]: {
    query: undefined;
    body: {
      uuid: string;
      name?: string;
      description?: string;
      logo?: File;
    };
    path: undefined;
  };
  [Endpoint.GetOrganizations]: {
    query: PaginationQuery & { my_organizations?: boolean };
    body: undefined;
    path: undefined;
  };
  [Endpoint.GetOrganization]: {
    query: { slug: string };
    body: undefined;
    path: undefined;
  };
  [Endpoint.GetInterviewQuestions]: {
    query: { interview_uuid: Interview["uuid"] };
    body: undefined;
    path: undefined;
  };
  [Endpoint.GetInterviewAssessments]: {
    query: { interview_uuid: Interview["uuid"] };
    body: undefined;
    path: undefined;
  };
  [Endpoint.GetInterviewAssessment]: {
    query: { interview_assessment_uuid: InterviewAssessment["uuid"] };
    body: undefined;
    path: undefined;
  };
  [Endpoint.GetMessages]: {
    query?: PaginationQuery;
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
  [Endpoint.GetSubscriptionStatus]: SubscriptionStatus;
  [Endpoint.ResetIndex]: null;
  [Endpoint.GetUserMetas]: UserMeta[];
  [Endpoint.PatchUserMeta]: UserMeta;
  [Endpoint.GetInterviews]: Interview[];
  [Endpoint.GetInterview]: Interview;
  [Endpoint.GetOnboarding]: Onboarding;
  [Endpoint.GetStandups]: Standup[];
  [Endpoint.GetNotifications]: Notification[];
  [Endpoint.GetSuggestion]: { text: string };
  [Endpoint.GetFileUploadLink]: { upload_link: string; file_uuid: string };
  [Endpoint.ActivateFile]: File;
  [Endpoint.GetFiles]: File[];
  [Endpoint.GetFileDownloadLink]: { download_link: string };
  [Endpoint.UpdateUser]: User;
  [Endpoint.CreateOrganization]: Organization;
  [Endpoint.GetOrganization]: Organization;
  [Endpoint.UpdateOrganization]: Organization;
  [Endpoint.GetOrganizations]: Organization[];
  [Endpoint.GetInterviewQuestions]: InterviewQuestion[];
  [Endpoint.GetInterviewAssessments]: InterviewAssessment[];
  [Endpoint.GetInterviewAssessment]: InterviewAssessment;
  [Endpoint.GetMessages]: Message[];
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
