"use client";

import { useState, useEffect, useContext, useRef } from "react";
import { Alert, Button, Label, Modal, TextInput } from "flowbite-react";
import { useSocket } from "@/shared/useSocket";
import { GlobalContext } from "@/app/provider";
import { Loader } from "@/shared/loader";
import { addToast } from "@/shared/useStore/toast";
import { setAuthToken } from "@/api/auth";
import { setAuthenticated } from "@/shared/useStore/auth";

export const AuthButton = () => {
  const [awaitAuth, setAwaitAuth] = useState(false);
  const [form, setForm] = useState({
    values: {
      email: "",
    },
  });
  const {
    dispatch,
    store: { isAuthenticated },
  } = useContext(GlobalContext);
  const emailInput = useRef<HTMLInputElement>(null);

  const { handleSend, handleConnect, handleClose, connected, loading } =
    useSocket<
      { email: string },
      { success: boolean; message: string; token: string }
    >(`${process.env.NEXT_PUBLIC_SOCKET_URL}/auth-start`, {
      handleReceive: async (message) => {
        console.info(message);
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
    });

  useEffect(() => {
    if (!connected) return;
    return () => {
      handleClose();
    };
  }, []);

  const handleAuth = () => {
    handleSend(form.values);
  };

  const handleCloseModal = () => {
    const confirmed = window.confirm(
      "Are you sure you want to cancel logging in?",
    );
    if (confirmed) {
      handleClose();
      setAwaitAuth(false);
    }
  };

  if (isAuthenticated) return null;

  return (
    <>
      <Modal
        show={connected}
        size="md"
        popup
        onClose={handleCloseModal}
        initialFocus={emailInput}
      >
        <Modal.Header />
        <Modal.Body>
          {awaitAuth ? (
            <div className="space-y-2">
              <h3 className="text-lg font-bold dark:text-white">
                Check your email
              </h3>
              <Alert color="success">
                <h4 className="text-md font-bold">Logging in...</h4>
                <p className="text-sm">
                  We have sent you a magic link to your email. Click the link
                  from any device in order to continue here.{" "}
                  <strong>Do not close this prompt.</strong>
                </p>
              </Alert>
              <div className="rounded-md border border-gray-200 p-4 dark:text-white">
                <Loader message="Great things are happening." />
              </div>
            </div>
          ) : (
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
              <h3 className="text-xl font-bold dark:text-white">
                Register or Login
              </h3>
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
                  We will send you a magic link to your email to login or
                  register. Simply click the link from any device to continue
                  here.
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
          )}
        </Modal.Body>
      </Modal>
      <Button color="green" className="col-span-1" onClick={handleConnect}>
        Login/Register
      </Button>
    </>
  );
};
