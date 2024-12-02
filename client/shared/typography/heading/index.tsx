import { FC, HTMLAttributes, ReactNode } from "react";

interface HeadingProps extends HTMLAttributes<HTMLHeadingElement> {
  children: ReactNode;
}

export const Heading: FC<HeadingProps> = ({ children, ...props }) => {
  return (
    <span
      {...props}
      className={`text-black dark:text-white ${props.className}`}
    >
      {children}
    </span>
  );
};
