import {
  ApiAction,
  callApi,
  Response,
  Endpoint,
  EndpointResponse,
} from "@/api";
import { GlobalContext } from "@/app/provider";
import { useContext, useState } from "react";
import { addToast } from "../useStore/toast";

interface UseCallApiOptions {
  successMessage?: string;
  errorMessage?: string;
  revalidationPath?: Endpoint;
}

export const useCallApi = <E extends Endpoint>(
  apiAction: ApiAction<E>,
  options?: UseCallApiOptions,
) => {
  const [loading, setLoading] = useState(false);
  const [res, setRes] = useState<Response<EndpointResponse[E]> | null>(null);
  const { dispatch } = useContext(GlobalContext);

  const call = async () => {
    setLoading(true);
    try {
      const res = await callApi(apiAction, options?.revalidationPath);
      setRes(res);
      if (!res.success) {
        console.error("Failed Response: ", res);
        throw Error("Network error");
      }
      dispatch(
        addToast({
          type: "success",
          description: options?.successMessage || "Success!",
        }),
      );
      setLoading(false);
    } catch (err) {
      console.error(err);
      setLoading(false);

      dispatch(
        addToast({
          type: "error",
          description: options?.errorMessage || "Something went wrong",
        }),
      );
    }
  };

  return { call, res, loading };
};
