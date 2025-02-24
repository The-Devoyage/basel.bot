"use client";

import { Interview, Organization } from "@/types";
import { FC, createContext, useMemo } from "react";

interface InterviewPageContext {
  interview: Interview | null;
  organizations: Organization[];
}

export const InterviewPageContext = createContext<InterviewPageContext>({
  interview: null,
  organizations: [],
});

export const InterviewPageProvider: FC<{
  children: React.ReactNode;
  interview: Interview | null;
  organizations: Organization[];
}> = ({ children, interview, organizations }) => {
  const value = useMemo(
    () => ({ interview, organizations }),
    [interview, organizations],
  );

  return (
    <InterviewPageContext.Provider value={value}>
      {children}
    </InterviewPageContext.Provider>
  );
};
