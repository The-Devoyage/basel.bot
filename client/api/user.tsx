import { User } from "@/types/user";
import { Response } from "./";

export const fetchMe = async (token: string): Promise<Response<User>> => {
  const response = await fetch("http://localhost:8000/me", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  if (!response.ok) {
    throw new Error("Failed to fetch user");
  }
  return response.json();
};
