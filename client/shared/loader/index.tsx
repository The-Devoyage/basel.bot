import { FC } from "react";
import { BiSolidLeaf } from "react-icons/bi";

interface LoaderProps {
  message?: string;
}

export const Loader: FC<LoaderProps> = ({ message = "Loading..." }) => {
  return (
    <div className="flex h-full flex-col items-center justify-center space-y-4">
      <BiSolidLeaf className="h-12 w-12 animate-wiggle text-green-400" />
      <p>{message}</p>
    </div>
  );
};
