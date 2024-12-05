"use client";

import { useContext, useEffect, useRef, useState } from "react";
import { Alert, Button } from "flowbite-react";
import { BiSolidLeaf } from "react-icons/bi";
import { GlobalContext } from "@/app/provider";
import { useRouter } from "next/navigation";
import { Endpoint, callApi } from "@/api";
import { setAuthToken } from "@/api/auth";
import { setAuthenticated } from "@/shared/useStore/auth";

export default function Page({ params }: { params: { auth_token: string } }) {
  const router = useRouter();
  const {
    dispatch,
    store: { isAuthenticated },
  } = useContext(GlobalContext);
  const [message, setMessage] = useState<{
    type: "error" | "success";
    message: string;
  } | null>(null);
  const hasVerified = useRef(false);

  useEffect(() => {
    if (hasVerified.current) return;
    hasVerified.current = true;

    const finishAuth = async () => {
      try {
        const res = await callApi({
          endpoint: Endpoint.AuthFinish,
          method: "POST",
          query: null,
          body: { token: params.auth_token },
          path: null,
        });
        if (!res.success || !res) {
          setMessage({ type: "error", message: "Failed to login." });
          return;
        }
        setMessage({
          type: "success",
          message:
            "Account verified! Continue from your original tab or device.",
        });
        if (res.data?.token) {
          await setAuthToken(res.data.token);
          dispatch(setAuthenticated(true));
        }
      } catch (error) {
        setMessage({
          type: "error",
          message: "An error occurred, please try again.",
        });
      }
    };

    finishAuth();
  }, [params.auth_token]);

  return (
    <div className="flex w-full flex-col items-center justify-center">
      <Alert color="success" className="w-96">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-green-400">
            {!message
              ? "Verifying"
              : message.type === "error"
                ? "Error"
                : "Success"}
          </h1>
          <BiSolidLeaf className="my-4 h-8 w-8 animate-wiggle text-green-400" />
        </div>
        {!message ? (
          <p className="text-md text-gray-500">
            Verifying your account - Please wait...
          </p>
        ) : (
          <p
            className={`text-${message.type === "error" ? "red" : "green"}-500`}
          >
            {message.message}
          </p>
        )}
        {isAuthenticated && (
          <Button
            color="green"
            className="mt-2 w-full"
            onClick={() => {
              router.push("/");
            }}
          >
            Continue
          </Button>
        )}
      </Alert>
    </div>
  );
}
