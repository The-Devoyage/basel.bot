import { PageHeader } from "@/shared/layout/page-header";
import { CreateShareableLinkButton, ShareableLinksTable } from "./components";
import { Typography } from "@/shared/typography";
import { Alert } from "flowbite-react";
import { Endpoint, callApi } from "@/api";

const MyBaselPage = async () => {
  const shareableLinks = await callApi({
    endpoint: Endpoint.ShareableLinks,
    query: {
      limit: 10,
      offset: 0,
    },
    body: null,
  });

  return (
    <section className="flex w-full flex-col">
      <PageHeader title="My Basel" />
      <div className="mb-3 flex items-center justify-between">
        <Typography.Heading className="text-2xl">
          Shareable Links
        </Typography.Heading>
        <CreateShareableLinkButton />
      </div>
      <Alert color="info" className="mb-3">
        <Typography.Heading className="text-lg dark:!text-slate-900">
          Getting Noticed
        </Typography.Heading>
        <Typography.Paragraph className="dark:text-slate-700">
          Share your bot with others by simply sharing a link. Employers and
          recruiters can converse with your bot about you, allowing them to
          quickly match your skills to a position that is perfect for you.
        </Typography.Paragraph>
      </Alert>
      <ShareableLinksTable shareableLinks={shareableLinks.data} />
    </section>
  );
};

export default MyBaselPage;
