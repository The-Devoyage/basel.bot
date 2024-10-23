import { Dispatch, useEffect, useRef } from "react";
import { AppAction, AppState } from "../useStore";
import { addToken, removeToken } from "../useStore/auth";
import { addToast } from "../useStore/toast";

export const useVerifyLogin = (
  store: AppState,
  dispatch: Dispatch<AppAction>,
) => {
  const attemptVerify = useRef(false);

  useEffect(() => {
    const t = window.localStorage.getItem("token");
    if (!t) return;

    dispatch(addToken(t));

    const handleStorageChange = () => {
      const t = window.localStorage.getItem("token");
      if (!t) {
        dispatch(removeToken());
        return;
      }
      dispatch(addToken(t));
    };

    window.addEventListener("storage", handleStorageChange);

    return () => {
      window.removeEventListener("storage", handleStorageChange);
    };
  }, []);

  useEffect(() => {
    const watchToken = async () => {
      if (attemptVerify.current || !store.token) return;

      if (store.token) {
        attemptVerify.current = true;
        window.localStorage.setItem("token", store.token);

        const res = await fetch("http://localhost:8000/verify", {
          headers: {
            Authorization: `Bearer ${store.token}`,
            ContentType: "application/json",
          },
        });
        const data = await res.json();

        if (!data.success) {
          localStorage.removeItem("token");
          dispatch(removeToken());
          dispatch(
            addToast({
              type: "error",
              description: "You have been signed out. Please sign in again.",
            }),
          );
        }
      }
    };

    watchToken();
  }, [store.token]);
};
