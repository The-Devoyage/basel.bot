import { Loader } from "@/shared/loader";
import { Alert } from "flowbite-react";

export const AwaitAuth = () => {
  return (
    <div className="space-y-2">
      <h3 className="text-lg font-bold dark:text-white">Check your email</h3>
      <Alert color="success">
        <h4 className="text-md font-bold">Logging in...</h4>
        <p className="text-sm">
          We have sent you a magic link to your email. Click the link from any
          device in order to continue here.{" "}
          <strong>Do not close this prompt.</strong>
        </p>
      </Alert>
      <div className="rounded-md border border-gray-200 p-4 dark:text-white">
        <Loader message="Great things are happening, and you are part of them." />
      </div>
    </div>
  );
};
