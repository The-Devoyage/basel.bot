"use client";

import { Endpoint, callApi } from "@/api";
import { removeAuthToken } from "@/api/auth";
import { GlobalContext } from "@/app/provider";
import { setAuthenticated } from "@/shared/useStore/auth";
import { addToast } from "@/shared/useStore/toast";
import { Dropdown } from "flowbite-react";
import { useContext } from "react";
import { useRouter } from "next/navigation";

export const SignoutDropdownItem = () => {
  const { client, dispatch } = useContext(GlobalContext);
  const router = useRouter();

  const handleSignout = async () => {
    try {
      const response = await callApi({
        endpoint: Endpoint.Logout,
        method: "POST",
        query: null,
        body: null,
        path: null,
      });

      if (!response.success) {
        throw new Error("Failed to sign out.");
      }

      await removeAuthToken();

      client?.handleClose();

      dispatch(
        addToast({
          type: "success",
          description: "Successfully signed out.",
        }),
      );
      dispatch(setAuthenticated(false));
      router.push("/");
    } catch (error) {
      console.error(error);
      dispatch(
        addToast({
          type: "error",
          description: "An error occurred while signing out.",
        }),
      );
    }
  };
  return <Dropdown.Item onClick={handleSignout}>Sign out</Dropdown.Item>;
};
