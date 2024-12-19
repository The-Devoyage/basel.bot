import { PageHeader } from "@/shared/layout/page-header";
import {
  CreateShareableLinkButton,
  ShareableLinksTable,
  UserMetasTable,
} from "./components";
import { Typography } from "@/shared/typography";
import {
  Accordion,
  AccordionContent,
  AccordionPanel,
  AccordionTitle,
  Alert,
  Card,
} from "flowbite-react";
import { Endpoint, callApi } from "@/api";
import { ResetIndex } from "./components/reset-index";

const MyBaselPage = async () => {
  const shareableLinks = await callApi(
    {
      endpoint: Endpoint.ShareableLinks,
      query: {
        limit: 100,
        offset: 0,
      },
      body: null,
      path: null,
    },
    {
      tags: ["shareable-links"],
    },
  );

  return (
    <section className="flex w-full flex-col space-y-4">
      <PageHeader title="My Basel" />
      <Card>
        <Accordion>
          <AccordionPanel>
            <AccordionTitle>
              <div className="flex w-full items-center justify-between">
                <Typography.Heading className="text-2xl">
                  Shareable Links
                </Typography.Heading>
              </div>
            </AccordionTitle>
            <AccordionContent>
              <div className="space-y-3">
                <Alert color="blue" withBorderAccent>
                  <div className="mb-3 flex w-full items-start justify-between">
                    <Typography.Heading className="mt-0 text-lg dark:!text-slate-900">
                      Getting Noticed
                    </Typography.Heading>
                    <CreateShareableLinkButton />
                  </div>
                  <Typography.Paragraph className="dark:text-slate-700">
                    Share your bot with others by simply sharing a link.
                    Employers and recruiters can converse with your bot about
                    you, allowing them to quickly match your skills to a
                    position that is perfect for you.
                  </Typography.Paragraph>
                </Alert>
                <ShareableLinksTable shareableLinks={shareableLinks.data} />
              </div>
            </AccordionContent>
          </AccordionPanel>
          <AccordionPanel>
            <AccordionTitle>
              <div className="flex items-center justify-between">
                <Typography.Heading className="text-2xl">
                  Memory Index
                </Typography.Heading>
              </div>
            </AccordionTitle>
            <AccordionContent>
              <div className="space-y-3">
                <ResetIndex />
                <UserMetasTable />
              </div>
            </AccordionContent>
          </AccordionPanel>
        </Accordion>
      </Card>
    </section>
  );
};

export default MyBaselPage;
