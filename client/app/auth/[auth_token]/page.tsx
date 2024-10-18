"use client";

import { useEffect, useState } from "react";
import { Alert } from "flowbite-react";
import { BiSolidLeaf } from "react-icons/bi";

export default function Page({ params }: { params: { auth_token: string } }) {
  const [message, setMessage] = useState<{
    type: "error" | "success";
    message: string;
  } | null>(null);

  useEffect(() => {
    const verifyAccount = async () => {
      try {
        const res = await fetch("http://localhost:8000/auth-finish", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ token: params.auth_token }),
        });
        const data = await res.json();
        if (data.error || data.status_code !== 200) {
          setMessage({ type: "error", message: data.error || data.detail });
          return;
        }
        setMessage({
          type: "success",
          message:
            "Account verified! Continue from your original tab or device.",
        });
      } catch (error) {
        console.error(error);
        setMessage({
          type: "error",
          message: "An error occurred, please try again.",
        });
      }
    };

    verifyAccount();
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
      </Alert>
    </div>
  );
}
