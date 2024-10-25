export * from "./user";

export interface Response<T> {
  success: boolean;
  data: T | null;
}
