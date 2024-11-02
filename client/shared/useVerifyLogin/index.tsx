import { Dispatch, useEffect, useRef } from "react";
import { AppAction } from "../useStore";
import { verifyAuthToken } from "@/api/auth";
import { setAuthenticated } from "../useStore/auth";

export const useVerifyLogin = (dispatch: Dispatch<AppAction>) => {
  const hasChecked = useRef(false);
  useEffect(() => {
    const handleVerifyAuthToken = async () => {
      if (hasChecked.current) return;
      hasChecked.current = true;
      const isAuth = await verifyAuthToken();
      dispatch(setAuthenticated(isAuth.success));
    };

    handleVerifyAuthToken();
  }, []);
};
