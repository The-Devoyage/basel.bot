"use client";

import { GlobalContext } from "@/app/provider";
import { useSocket } from "@/shared/useSocket";
import { Alert, Button, Label, TextInput } from "flowbite-react";
import { setAuthToken } from "@/api/auth";
import { useContext, useEffect, useRef, useState } from "react";
import { setAuthenticated } from "@/shared/useStore/auth";
import { addToast } from "@/shared/useStore/toast";
import { AwaitAuth } from "./components";
import { redirect, useSearchParams } from "next/navigation";

export const AuthForm = () => {
  const [awaitAuth, setAwaitAuth] = useState(false);
  const [form, setForm] = useState({
    values: {
      email: "",
    },
  });
  const {
    dispatch,
    store: {
      auth: { isAuthenticated },
    },
  } = useContext(GlobalContext);
  const emailInput = useRef<HTMLInputElement>(null);
  const searchParams = useSearchParams();
  const redirectUri = searchParams.get("redirect_uri");

  const { handleSend, handleConnect, handleClose, loading } = useSocket<
    { email: string },
    { success: boolean; message: string; token: string }
  >(`${process.env.NEXT_PUBLIC_SOCKET_URL}/auth-start`, {
    onReceive: async (message) => {
      if (message?.token) {
        await setAuthToken(message.token);
        dispatch(setAuthenticated(true));
        dispatch(
          addToast({
            type: "success",
            description: message?.message,
          }),
        );
        handleClose();
      }

      if (!message?.success) {
        dispatch(addToast({ type: "error", description: message?.message }));
        dispatch(setAuthenticated(false));
      } else {
        setAwaitAuth(true);
      }
    },
    onClose: () => {
      setAwaitAuth(false);
    },
  });

  useEffect(() => {
    handleConnect();
    return () => {
      handleClose();
    };
  }, []);

  useEffect(() => {
    if (isAuthenticated) return redirect(redirectUri || "/");
  }, [isAuthenticated]);

  const handleAuth = () => {
    handleSend(form.values, true, false, false);
  };

  if (awaitAuth) {
    return <AwaitAuth />;
  }

  return (
    <form
      className="space-y-6"
      onSubmit={(e) => {
        e.preventDefault();
      }}
      onKeyUp={(e) => {
        e.preventDefault();
        if (e.key === "Enter") {
          handleAuth();
        }
      }}
    >
      <h3 className="text-xl font-bold dark:text-white">Register or Login</h3>
      <div className="flex flex-col space-y-2">
        <Label>Your Email</Label>
        <TextInput
          type="email"
          ref={emailInput}
          placeholder="example@email.com"
          className="col-span-3"
          value={form.values.email}
          onChange={(e) =>
            setForm((prev) => ({
              ...prev,
              values: { ...prev.values, email: e.target.value },
            }))
          }
        />
      </div>
      <Alert color="info">
        <h4 className="text-md font-bold">Magic Links</h4>
        <p className="text-sm">
          We will send you a magic link to your email to login or register.
          Simply click the link from any device to continue here.
        </p>
      </Alert>
      <Button
        color="green"
        isProcessing={loading}
        onClick={handleAuth}
        className="w-full"
      >
        Submit
      </Button>
    </form>
  );
};
