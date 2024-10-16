import { AnchorHTMLAttributes, FC } from "react";

interface LinkProps extends AnchorHTMLAttributes<HTMLAnchorElement> {
  children: React.ReactNode;
}

export const Link: FC<LinkProps> = ({ children, ...props }) => {
  return (
    <a {...props} className={`text-black dark:text-white ${props.className}`}>
      {children}
    </a>
  );
};
