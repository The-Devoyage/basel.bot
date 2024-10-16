"use client";

import { useState, useEffect, useContext } from "react";
import { Alert, Button, Label, Modal, TextInput } from "flowbite-react";
import { useSocket } from "@/shared/useSocket";
import { GlobalContext } from "@/app/provider";
import { v4 } from "uuid";
import { Loader } from "@/shared/loader";

export const Auth = () => {
  const [awaitAuth, setAwaitAuth] = useState(false);
  const [form, setForm] = useState({
    values: {
      email: "",
    },
  });

  const { dispatch } = useContext(GlobalContext);

  const {
    handleSend,
    initializing,
    handleConnect,
    handleClose,
    connected,
    loading,
  } = useSocket<
    { email: string },
    { success: boolean; message: string; jwt: string }
  >("ws://localhost:8000/register-start", {
    handleReceive: (message) => {
      if (message?.jwt) {
        localStorage.setItem("jwt", message.jwt);
        dispatch?.({
          type: "ADD_TOAST",
          payload: {
            uuid: v4(),
            type: "success",
            description: "You have successfully logged in.",
          },
        });
        handleClose();
      }

      if (!message?.success) {
        dispatch?.({
          type: "ADD_TOAST",
          payload: {
            uuid: v4(),
            type: "error",
            description: message?.message,
          },
        });
      } else {
        setAwaitAuth(true);
      }
    },
  });

  useEffect(() => {
    return () => {
      handleClose();
    };
  }, []);

  const handleAuth = () => {
    handleSend(form.values);
  };

  return (
    <>
      <Modal show={connected} size="md" popup onClose={handleClose}>
        <Modal.Header />
        <Modal.Body>
          {awaitAuth ? (
            <div className="space-y-2">
              <h3 className="text-lg font-bold">Check your email</h3>
              <Alert color="success">
                <h4 className="text-md font-bold">Logging in...</h4>
                <p className="text-sm">
                  We have sent you a magic link to your email. Click the link in
                  your email on any device in order to continue here.{" "}
                  <strong>Do not close this window.</strong>
                </p>
              </Alert>
              <div className="rounded-md border border-gray-200 p-4">
                <Loader message="Great things are happening." />
              </div>
            </div>
          ) : (
            <form
              className="space-y-6"
              onSubmit={(e) => {
                e.preventDefault();
              }}
            >
              <h3 className="text-xl font-bold">Register or Login</h3>
              <div className="flex flex-col space-y-2">
                <Label>Your Email</Label>
                <TextInput
                  type="email"
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
                  We will send you a magic link to your email to login or
                  register. Simply click the link from any device to continue
                  here.
                </p>
              </Alert>
              <Button color="green" isProcessing={loading} onClick={handleAuth}>
                Submit
              </Button>
            </form>
          )}
        </Modal.Body>
      </Modal>
      <Button
        color="green"
        className="col-span-1"
        isProcessing={initializing}
        onClick={handleConnect}
      >
        Login/Register
      </Button>
    </>
  );
};
