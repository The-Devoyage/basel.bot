import { Typography } from "@/shared/typography";
import { FC } from "react";

interface PageHeaderProps {
  title: string;
}

export const PageHeader: FC<PageHeaderProps> = ({ title }) => {
  return (
    <div className="mb-3">
      <Typography.Heading className="text-3xl">{title}</Typography.Heading>
    </div>
  );
};
