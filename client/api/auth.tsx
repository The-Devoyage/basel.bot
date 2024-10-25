"use server";

import { cookies } from "next/headers";

// Set auth token cookie
export const setAuthToken = async (token: string) => {
  const cookieStore = cookies();

  cookieStore.set({
    name: "token",
    value: token,
    httpOnly: true,
    path: "/",
    expires: new Date(Date.now() + 1000 * 60 * 60 * 24),
  });
};

export const removeAuthToken = async () => {
  const cookieStore = cookies();

  try {
    const res = await fetch("http://localhost:8000/logout", {
      method: "POST",
      headers: {
        ContentType: "application/json",
        Cookie: `token=${cookieStore.get("token")?.value}`,
      },
    });
    const data = await res.json();

    if (!data.success) {
      throw new Error(data.error || data.detail);
    }

    cookieStore.delete({
      name: "token",
    });

    return true;
  } catch (error) {
    console.error(error);
    return false;
  }
};

export const verifyAuthToken = async (): Promise<{ success: boolean }> => {
  const cookieStore = cookies();
  try {
    const res = await fetch("http://localhost:8000/verify", {
      headers: {
        ContentType: "application/json",
        Cookie: `token=${cookieStore.get("token")?.value}`,
      },
    });

    if (!res.ok) {
      cookieStore.delete({
        name: "token",
      });
      return { success: false };
    }

    const data = await res.json();

    return data;
  } catch (error) {
    console.error(error);
    return { success: false };
  }
};
