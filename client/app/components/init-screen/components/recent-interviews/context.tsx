"use client";

import { Endpoint } from "@/api";
import { GlobalContext } from "@/app/provider";
import { useCallApi } from "@/shared/useCallApi";
import { Interview } from "@/types";
import {
  Dispatch,
  FC,
  SetStateAction,
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";

interface InterviewContext {
  isTakenByMe: boolean;
  setIsTakenByMe: Dispatch<SetStateAction<boolean>>;
  interviews: Interview[];
  loading: boolean;
}

export const InterviewsContext = createContext<InterviewContext>({
  isTakenByMe: false,
  setIsTakenByMe: () => null,
  interviews: [],
  loading: false,
});

export const InterviewContextProvider: FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [isTakenByMe, setIsTakenByMe] = useState(false);
  const { slToken } = useContext(GlobalContext);
  const { call, res, loading } = useCallApi({
    endpoint: Endpoint.GetInterviews,
    query: {
      limit: 6,
      taken_by_me: !!slToken || isTakenByMe,
      sl_token: slToken || undefined,
    },
    body: null,
    path: null,
  });
  const interviews = res?.data || [];

  useEffect(() => {
    call();
  }, [isTakenByMe]);

  const value = useMemo(
    () => ({
      isTakenByMe,
      setIsTakenByMe,
      interviews,
      loading,
    }),
    [isTakenByMe, interviews, loading],
  );

  return (
    <InterviewsContext.Provider value={value}>
      {children}
    </InterviewsContext.Provider>
  );
};
