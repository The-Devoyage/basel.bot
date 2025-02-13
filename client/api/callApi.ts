"use server";

import { cookies } from "next/headers";
import { ApiAction, Endpoint, EndpointResponse, Response } from ".";
import qs from "qs";
import { revalidatePath, revalidateTag } from "next/cache";

export interface CallApiOptions {
  revalidationPath?: Endpoint;
  revalidationTag?: string;
  tags?: NextFetchRequestConfig["tags"];
}

export const callApi = async <E extends Endpoint>(
  { endpoint, method = "GET", query, body, path }: ApiAction<E>,
  options?: CallApiOptions,
): Promise<Response<EndpointResponse[E]>> => {
  // Handle Headers
  const cookieStore = await cookies();
  const token = cookieStore.get("token")?.value;
  const headers: HeadersInit = {
    "Content-Type": "application/json",
  };
  if (token) {
    headers.Cookie = `token=${cookieStore.get("token")?.value}`;
  }

  // Format Query String
  const queryString = query
    ? "?" + qs.stringify(query, { arrayFormat: "repeat" })
    : "";

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
      queryString,
      path,
      formattedEndpoint,
    });

    const res = await fetch(
      `${process.env.API_URL}${formattedEndpoint}${queryString}`,
      {
        method,
        body: body ? JSON.stringify(body) : undefined,
        headers,
        next: {
          tags: options?.tags,
        },
      },
    );

    if (!res.ok) {
      console.info("Network Error: ", res);
      throw new Error("Failed to call api.");
    }

    const data = await res.json();

    console.info("API Call Successful:", formattedEndpoint, data);

    if (options?.revalidationPath) {
      revalidatePath(options.revalidationPath);
    }

    if (options?.revalidationTag) {
      console.log("REVALIDATING TAG:", options.revalidationTag);
      revalidateTag(options.revalidationTag);
    }

    return data;
  } catch (err) {
    console.error(err);
    return { success: false, data: null };
  }
};
