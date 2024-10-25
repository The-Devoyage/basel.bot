"use server";

import { User } from "@/types/user";
import { Response } from "./";
import { cookies } from "next/headers";

export const fetchMe = async (): Promise<Response<User>> => {
  const cookieStore = cookies();

  try {
    const response = await fetch("http://localhost:8000/me", {
      headers: {
        ContentType: "application/json",
        Cookie: `token=${cookieStore.get("token")?.value}`,
      },
    });

    if (!response.ok) {
      throw new Error("Failed to fetch user");
    }

    return response.json();
  } catch (error) {
    console.error(error);
    return { success: false, data: null };
  }
};
