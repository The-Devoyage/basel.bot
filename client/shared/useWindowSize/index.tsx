"use client";

import { useEffect, useState } from "react";

export const useWindowSize = () => {
  const [windowSize, setWindowSize] = useState<{
    width: number | undefined;
    height: number | undefined;
  }>({
    width: undefined,
    height: undefined,
  });
  const isMobile = !!windowSize.width && windowSize.width < 768;

  useEffect(() => {
    function handleResize() {
      setWindowSize(getSize());
    }

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const getSize = () => {
    return {
      width: window.innerWidth,
      height: window.innerHeight,
    };
  };

  return {
    windowSize,
    isMobile,
  };
};
