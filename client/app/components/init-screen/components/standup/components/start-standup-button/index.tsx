"use client";

import { Button, Modal } from "flowbite-react";
import { TfiWrite } from "react-icons/tfi";
import { useHandleMessage } from "../../..";
import { Typography } from "@/shared/typography";
import dayjs from "dayjs";
import { useContext, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { FaX } from "react-icons/fa6";
import { GlobalContext } from "@/app/provider";

export const StartStandupButton = () => {
  const [visible, setVisible] = useState(false);
  const {
    store: {
      auth: { isAuthenticated },
    },
  } = useContext(GlobalContext);
  const { handleMessage } = useHandleMessage();
  const searchParams = useSearchParams();
  const standup = searchParams.get("standup");

  useEffect(() => {
    if (standup) setVisible(true);
  }, [standup]);

  const handleClick = () => {
    handleMessage(isAuthenticated ? "standup" : "describe_standup");
    setVisible(false);
  };

  return (
    <>
      <Modal show={visible} onClose={() => setVisible(false)}>
        <Modal.Body className="space-y-4">
          <Typography.Heading className="text-lg">
            Standup: {dayjs().format("dddd MMMM DD, YYYY")}
          </Typography.Heading>
          <Typography.Paragraph>
            Start your daily standup now or log one later.
          </Typography.Paragraph>
          <div className="flex gap-2">
            <Button
              gradientMonochrome="failure"
              className="flex items-center"
              outline
              onClick={() => {
                setVisible(false);
              }}
            >
              <FaX />
            </Button>
            <Button
              gradientDuoTone="redToYellow"
              outline
              onClick={handleClick}
              className="w-full"
            >
              <TfiWrite className="mr-2 h-5 w-5" /> Start Standup
            </Button>
          </div>
        </Modal.Body>
      </Modal>
      <Button gradientDuoTone="redToYellow" outline onClick={handleClick}>
        <TfiWrite className="h-5 w-5" />
      </Button>
    </>
  );
};
