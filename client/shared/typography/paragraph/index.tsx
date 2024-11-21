import { FC, HTMLAttributes, ReactNode } from "react";

interface ParagraphProps extends HTMLAttributes<HTMLParagraphElement> {
  children?: ReactNode;
}

export const Paragraph: FC<ParagraphProps> = ({ children, ...props }) => {
  return (
    <p
      {...props}
      className={`text-gray-600 dark:text-gray-300 ${props.className}`}
    >
      {children}
    </p>
  );
};
