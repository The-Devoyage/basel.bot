import { PageHeader } from "@/shared/layout/page-header";
import { ShareableLinksTable } from "./components";
import { Typography } from "@/shared/typography";
import { Alert, Button } from "flowbite-react";
import { BsPlusLg } from "react-icons/bs";

const MyBaselPage = () => {
  return (
    <section className="flex w-full flex-col">
      <PageHeader title="My Basel" />
      <div className="mb-3 flex items-center justify-between">
        <Typography.Heading className="text-2xl">
          Shareable Links
        </Typography.Heading>
        <Button color="success">
          <BsPlusLg />
        </Button>
      </div>
      <Alert color="info" className="mb-3">
        <Typography.Heading className="text-lg dark:text-slate-800">
          Getting Noticed
        </Typography.Heading>
        <Typography.Paragraph className="dark:text-slate-500">
          Share your bot with others by simply sharing a link. Employers and
          recruiters can converse with your bot about you, allowing them to
          quickly match your skills to a position that is perfect for you.
        </Typography.Paragraph>
      </Alert>
      <ShareableLinksTable />
    </section>
  );
};

export default MyBaselPage;
