import {
  ApiAction,
  callApi,
  Response,
  Endpoint,
  EndpointResponse,
} from "@/api";
import { GlobalContext } from "@/app/provider";
import { useContext, useState, useEffect } from "react";
import { addToast } from "../useStore/toast";

interface UseCallApiOptions<E extends Endpoint> {
  successMessage?: string;
  errorMessage?: string;
  revalidationPath?: Endpoint;
  onSuccess?: (response: Response<EndpointResponse[E]>) => void;
  onError?: (error: unknown) => void;
  callOnMount?: boolean;
}

export const useCallApi = <E extends Endpoint>(
  apiAction: ApiAction<E>,
  options?: UseCallApiOptions<E>,
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
        dispatch(addToast({ type: "error", description: res.message || "" }));
        options?.onError?.(res);
        return;
      }
      dispatch(
        addToast({
          type: "success",
          description: options?.successMessage || "Success!",
        }),
      );
      setLoading(false);
      options?.onSuccess?.(res);
      return res;
    } catch (err) {
      console.error(err);
      setLoading(false);
      options?.onError?.(err);
      dispatch(
        addToast({
          type: "error",
          description: options?.errorMessage || "Something went wrong",
        }),
      );
    }
  };

  useEffect(() => {
    if (options?.callOnMount) call();
  }, []);

  return { call, res, loading };
};
