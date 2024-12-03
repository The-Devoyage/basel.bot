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
    domain: process.env.NODE_ENV === "production" ? ".basel.bot" : undefined,
    secure: process.env.NODE_ENV === "production" ? true : undefined,
    sameSite: process.env.NODE_ENV === "production" ? "none" : undefined,
    expires: new Date(Date.now() + 1000 * 60 * 60 * 24 * 7),
  });
};

export const removeAuthToken = async () => {
  const cookieStore = cookies();

  cookieStore.delete({
    name: "token",
  });
};
