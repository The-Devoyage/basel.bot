import {
  ApiAction,
  callApi,
  Response,
  Endpoint,
  EndpointResponse,
  CallApiOptions,
} from "@/api";
import { GlobalContext } from "@/app/provider";
import { useContext, useState, useEffect } from "react";
import { addToast } from "../useStore/toast";

interface UseCallApiOptions<E extends Endpoint> {
  successMessage?: string;
  errorMessage?: string;
  onSuccess?: (response: Response<EndpointResponse[E]>) => void;
  onError?: (error: unknown) => void;
  callOnMount?: boolean;
  toast?: {
    onSuccess: boolean;
  };
  callApiOptions?: CallApiOptions;
}

export const useCallApi = <E extends Endpoint>(
  apiAction: ApiAction<E>,
  options?: UseCallApiOptions<E>,
) => {
  const [loading, setLoading] = useState(false);
  const [res, setRes] = useState<Response<EndpointResponse[E]> | null>(null);
  const { dispatch } = useContext(GlobalContext);

  const call = async (
    override?: Pick<ApiAction<E>, "body" | "path" | "query">,
  ) => {
    setLoading(true);
    try {
      const res = await callApi(
        { ...apiAction, ...override },
        options?.callApiOptions,
      );
      setRes(res);
      if (!res.success) {
        dispatch(addToast({ type: "error", description: res.message || "" }));
        options?.onError?.(res);
        return;
      }
      if (options?.toast?.onSuccess) {
        dispatch(
          addToast({
            type: "success",
            description: options?.successMessage || "Success!",
          }),
        );
      }
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
