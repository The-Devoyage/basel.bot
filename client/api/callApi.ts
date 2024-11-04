"use server";

import { cookies } from "next/headers";
import { ApiAction, Endpoint, EndpointResponse, Response } from ".";
import qs from "qs";
import { revalidatePath } from "next/cache";

export const callApi = async <E extends Endpoint>(
  { endpoint, method = "GET", query, body, path }: ApiAction<E>,
  revalidationPath?: Endpoint,
): Promise<Response<EndpointResponse[E]>> => {
  // Handle Headers
  const cookieStore = cookies();
  const token = cookieStore.get("token")?.value;
  const headers: HeadersInit = {
    "Content-Type": "application/json",
  };
  if (token) {
    headers.Cookie = `token=${cookieStore.get("token")?.value}`;
  }

  // Format Query String
  const queryString = query ? "?" + qs.stringify(query) : "";

  // Format Params
  let formattedEndpoint = endpoint as string;
  if (path) {
    for (const entry of Object.entries(path)) {
      formattedEndpoint = formattedEndpoint.replace(
        `:${entry[0]}`,
        entry[1] as any,
      );
    }
  }

  try {
    console.debug("Calling API: ", {
      endpoint,
      headers,
      method,
      body,
      query,
      path,
      formattedEndpoint,
    });
    const res = await fetch(
      `http://localhost:8000${formattedEndpoint}${queryString}`,
      {
        method,
        body: body ? JSON.stringify(body) : undefined,
        headers,
      },
    );

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
