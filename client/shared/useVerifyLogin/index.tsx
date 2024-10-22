import { Dispatch, useEffect, useRef } from "react";
import { v4 } from "uuid";
import { AppAction } from "../useStore";

export const useVerifyLogin = (
  dispatch: Dispatch<AppAction>,
  setToken?: React.Dispatch<React.SetStateAction<string | null>>,
) => {
  const isVerified = useRef(false);
  useEffect(() => {
    const watchToken = async () => {
      const token = localStorage.getItem("token");

      if (isVerified.current || !token) return;

      if (token) {
        isVerified.current = true;

        const res = await fetch("http://localhost:8000/verify", {
          headers: {
            Authorization: `Bearer ${token}`,
            ContentType: "application/json",
          },
        });
        const data = await res.json();
        if (!data.success) {
          localStorage.removeItem("token");
          setToken?.(null);
          dispatch?.({
            type: "ADD_TOAST",
            payload: {
              notification: {
                uuid: v4(),
                type: "error",
                description: "You have been signed out. Please sign in again.",
              },
            },
          });
        }
      }
    };

    watchToken();

    window.addEventListener("storage", watchToken);

    return () => {
      window.removeEventListener("storage", watchToken);
    };
  }, []);
};
