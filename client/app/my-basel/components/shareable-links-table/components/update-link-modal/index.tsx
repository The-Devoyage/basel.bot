"use client";

import { Endpoint } from "@/api";
import { MultiSelect } from "@/shared/multi-select";
import { useCallApi } from "@/shared/useCallApi";
import { ShareableLink } from "@/types";
import {
  Button,
  Label,
  Modal,
  TextInput,
  ToggleSwitch,
  Tooltip,
} from "flowbite-react";
import { FC, useEffect, useState } from "react";
import { TbInfoSquareFilled } from "react-icons/tb";

interface FormValues {
  interview_uuids: string[];
  status: boolean;
  tag: string;
}

export const UpdateLinkModal: FC<{
  show: boolean;
  shareableLink: ShareableLink | null;
  onClose: () => void;
}> = ({ show, onClose, shareableLink }) => {
  const [formValues, setFormValues] = useState<FormValues>({
    interview_uuids: [],
    status: false,
    tag: "",
  });
  const interviewsRes = useCallApi(
    {
      endpoint: Endpoint.GetInterviews,
      body: null,
      path: null,
      query: {
        limit: 0,
        taken_by_me: true,
      },
    },
    {
      callOnMount: true,
    },
  );
  const { call } = useCallApi(
    {
      endpoint: Endpoint.UpdateShareableLink,
      method: "PATCH",
      path: {
        uuid: shareableLink?.uuid!,
      },
      body: {
        status: formValues.status,
        tag: formValues.tag,
        interview_uuids: formValues.interview_uuids,
      },
      query: null,
    },
    {
      successMessage: "Updated Shareable Link",
      toast: {
        onSuccess: true,
      },
      callApiOptions: {
        revalidationTag: "shareable-links",
      },
      onSuccess: () => onClose(),
    },
  );

  useEffect(() => {
    if (!shareableLink) return;
    setFormValues({
      interview_uuids: shareableLink.interviews.map((i) => i.uuid),
      status: shareableLink.status,
      tag: shareableLink.tag,
    });
  }, [shareableLink]);

  const interviewOptions =
    interviewsRes.res?.data?.map((i) => ({
      label: i.position + " - " + i.organization?.name,
      value: i.uuid,
    })) || [];

  const handleSubmit = async () => {
    await call();
  };

  const handleChangeInterviews = (opt: string) => {
    if (formValues.interview_uuids.includes(opt)) {
      setFormValues((curr) => ({
        ...formValues,
        interview_uuids: [...curr.interview_uuids.filter((i) => i !== opt)],
      }));
    } else {
      setFormValues((curr) => ({
        ...formValues,
        interview_uuids: [...curr.interview_uuids, opt],
      }));
    }
  };

  if (!shareableLink) return null;

  return (
    <Modal show={show} onClose={onClose}>
      <Modal.Header>Edit Link</Modal.Header>
      <Modal.Body className="space-y-4">
        <div>
          <Label>Tag</Label>
          <TextInput
            type="text"
            placeholder={shareableLink.tag}
            value={formValues.tag}
            onChange={(e) =>
              setFormValues({ ...formValues, tag: e.currentTarget.value })
            }
          />
        </div>
        <div>
          <div className="flex justify-between">
            <Label>Interviews</Label>
            <Tooltip
              content="Attach interviews you have completed for recruiters to see when visiting your profile."
              placement="top-start"
            >
              <TbInfoSquareFilled className="size-6 dark:text-white" />
            </Tooltip>
          </div>
          <MultiSelect
            options={interviewOptions}
            value={formValues.interview_uuids}
            onChange={handleChangeInterviews}
          />
        </div>
      </Modal.Body>
      <Modal.Footer className="flex justify-between">
        <ToggleSwitch
          checked={formValues?.status}
          onChange={(s) => setFormValues({ ...formValues, status: s })}
          color="green"
          label="Status"
        />
        <Button outline color="green" onClick={handleSubmit}>
          Save
        </Button>
      </Modal.Footer>
    </Modal>
  );
};
