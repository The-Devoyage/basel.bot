"use client";

import { Endpoint } from "@/api";
import { useHandleMessage } from "@/app/components/init-screen/components";
import { Typography } from "@/shared/typography";
import { useCallApi } from "@/shared/useCallApi";
import { Button, Card, Textarea } from "flowbite-react";
import { forwardRef, useEffect, useState } from "react";

export const InterviewQuestionCard = forwardRef<
  HTMLDivElement,
  { message: string }
>(({ message }, ref) => {
  const [value, setValue] = useState("");
  const cardData = JSON.parse(message);
  const { handleMessage } = useHandleMessage();
  const { call, loading } = useCallApi(
    {
      endpoint: Endpoint.UpsertInterviewQuestionResponse,
      method: "POST",
      query: null,
      path: {
        interview_question_uuid: "",
      },
      body: {
        response: "",
      },
    },
    {
      onSuccess: () => {
        handleMessage("next_question");
      },
    },
  );

  useEffect(() => {
    if (cardData.response) setValue(cardData.response);
    console.log(cardData);
  }, [message]);

  const handleSubmit = async () => {
    await call({
      body: {
        response: value,
      },
      path: {
        interview_question_uuid: cardData.interview_question.uuid,
      },
      query: null,
    });
  };

  return (
    <div ref={ref} className="w-full">
      <Card className="border-2 border-purple-400 dark:border-purple-600">
        <div className="flex flex-row items-center space-x-4">
          <Typography.Heading className="text-xl capitalize">
            {cardData.header || "Question"}
          </Typography.Heading>
        </div>
        <Typography.Paragraph>
          {cardData.interview_question.question}
        </Typography.Paragraph>
        <Textarea
          color="purple"
          placeholder="Write your answer here..."
          value={value}
          onChange={(e) => setValue(e.currentTarget.value)}
          disabled={loading}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              handleSubmit();
            }
          }}
          theme={{
            colors: {
              purple: "border-2 border-purple-400 focus:border-purple-600",
            },
          }}
        />
        <div className="flex items-center justify-end">
          <Button
            gradientMonochrome="purple"
            outline
            onClick={handleSubmit}
            isProcessing={loading}
          >
            Save
          </Button>
        </div>
      </Card>
    </div>
  );
});
