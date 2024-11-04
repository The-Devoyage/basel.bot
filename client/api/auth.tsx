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

  cookieStore.delete({
    name: "token",
  });
};
