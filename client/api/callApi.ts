"use server";

import { cookies } from "next/headers";
import { ApiAction, Endpoint, EndpointResponse, Response } from ".";
import qs from "qs";
import { revalidatePath } from "next/cache";

export const callApi = async <E extends Endpoint>(
  { endpoint, method = "GET", query, body }: ApiAction<E>,
  revalidationPath?: Endpoint,
): Promise<Response<EndpointResponse[E]>> => {
  const cookieStore = cookies();
  const queryString = query ? "?" + qs.stringify(query) : "";
  const token = cookieStore.get("token")?.value;
  const headers: HeadersInit = {
    "Content-Type": "application/json",
  };
  if (token) {
    headers.Cookie = `token=${cookieStore.get("token")?.value}`;
  }

  try {
    console.debug("Calling API: ", {
      endpoint,
      headers,
      method,
      body,
      query,
    });
    const res = await fetch(`http://localhost:8000${endpoint}${queryString}`, {
      method,
      body: body ? JSON.stringify(body) : undefined,
      headers,
    });

    if (!res.ok) {
      console.info("Network Error: ", res);
      throw new Error("Failed to call api.");
    }

    const data = await res.json();

    console.info("API Call Successful: ", data);

    if (revalidationPath) {
      revalidatePath(revalidationPath);
    }

    return data;
  } catch (err) {
    console.error(err);
    return { success: false, data: null };
  }
};
