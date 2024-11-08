"use client";

import { Dispatch } from "react";
import { AppAction } from "../useStore";
import { Endpoint } from "@/api";
import { setAuthenticated } from "../useStore/auth";
import { useCallApi } from "../useCallApi";

export const useVerifyLogin = (dispatch: Dispatch<AppAction>) => {
  useCallApi(
    {
      endpoint: Endpoint.Verify,
      query: null,
      body: null,
      path: null,
    },
    {
      callOnMount: true,
      onSuccess: () => {
        dispatch(setAuthenticated(true));
      },
    },
  );
};
