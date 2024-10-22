import { User } from "@/types/user";
import { useContext, useEffect, useState } from "react";
import { Response } from "./";
import { GlobalContext } from "@/app/provider";
import { SET_ME, setMe } from "@/shared/useStore/auth";

export const fetchMe = async (token: string): Promise<Response<User>> => {
  const response = await fetch("http://localhost:8000/me", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  if (!response.ok) {
    throw new Error("Failed to fetch user");
  }
  return response.json();
};

export const useGetUser = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  const { store, dispatch } = useContext(GlobalContext);

  useEffect(() => {
    if (!store.token) {
      return;
    }
    fetchMe(store.token)
      .then((user) => {
        setUser(user.data);
      })
      .catch((error) => {
        setError(error);
      })
      .finally(() => {
        setLoading(false);
      });

    return () => {
      setLoading(true);
      setError(null);
    };
  }, [store.token]);

  useEffect(() => {
    dispatch(setMe(user));
  }, [user]);

  return { user, loading, error };
};
