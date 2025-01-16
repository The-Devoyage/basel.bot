import { Typography } from "@/shared/typography";
import { Card } from "flowbite-react";

export const EmptyFiles = () => {
  return (
    <Card>
      <Typography.Heading className="text-xl">
        Nothing Found!
      </Typography.Heading>
      <Typography.Paragraph>Upload a file to get started.</Typography.Paragraph>
    </Card>
  );
};
