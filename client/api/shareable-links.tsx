"use server";

import { ShareableLink } from "@/types/shareable-link";
import { Response } from "./";
import { cookies } from "next/headers";

export const getShareableLinks = async (): Promise<
  Response<ShareableLink[]>
> => {
  const cookieStore = cookies();

  try {
    const res = await fetch(
      "http://localhost:8000/shareable-links?limit=10&offset=0",
      {
        headers: {
          ContentType: "application/json",
          Cookie: `token=${cookieStore.get("token")?.value}`,
        },
      },
    );

    if (!res.ok) {
      throw new Error("Failed to fetch shareable links");
    }

    return res.json();
  } catch (err) {
    console.log(err);
    return { success: false, data: null };
  }
};
