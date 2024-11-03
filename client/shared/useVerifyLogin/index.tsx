import { Dispatch, useEffect, useRef } from "react";
import { AppAction } from "../useStore";
import { Endpoint, callApi } from "@/api";
import { setAuthenticated } from "../useStore/auth";

export const useVerifyLogin = (dispatch: Dispatch<AppAction>) => {
  const hasChecked = useRef(false);
  useEffect(() => {
    const handleVerifyAuthToken = async () => {
      if (hasChecked.current) return;
      hasChecked.current = true;
      const isAuth = await callApi({
        endpoint: Endpoint.Verify,
        query: null,
        body: null,
      });
      dispatch(setAuthenticated(isAuth.success));
    };

    handleVerifyAuthToken();
  }, []);
};
