"use client";

import { useContext, useEffect, useState } from "react";
import { OrganizationForm, OrganizationsPageContext } from "../../context";
import { Button, Label, Modal, TextInput, Textarea } from "flowbite-react";
import { FileManager } from "@/shared/file-manager";
import { TiAttachmentOutline } from "react-icons/ti";
import Image from "next/image";
import { ValidMimeType } from "@/types";

const initialForm: OrganizationForm = {
  name: "",
  description: "",
  logo: null,
};

export const EditOrganizationModal = () => {
  const {
    showEditOrganizationModal,
    toggleEditOrganizationModal,
    handleCreateOrganization,
    handleUpdateOrganization,
    selectedOrganization,
  } = useContext(OrganizationsPageContext);
  const [showFileManager, setShowFileManager] = useState(false);
  const [form, setForm] = useState<OrganizationForm>(initialForm);

  useEffect(() => {
    if (selectedOrganization) {
      setForm({
        uuid: selectedOrganization.uuid,
        name: selectedOrganization.name,
        description: selectedOrganization.description,
        logo: selectedOrganization.logo ?? null,
      });
    }
  }, [selectedOrganization]);

  useEffect(() => {
    if (!showEditOrganizationModal) {
      setForm(initialForm);
    }
  }, [showEditOrganizationModal]);

  const toggleFileManager = () => {
    setShowFileManager(!showFileManager);
  };

  const handleSubmit = async () => {
    if (form.uuid) {
      await handleUpdateOrganization(form, () => setForm(initialForm));
    } else {
      await handleCreateOrganization(form, () => setForm(initialForm));
    }
  };

  return (
    <Modal
      show={showEditOrganizationModal}
      onClose={toggleEditOrganizationModal}
    >
      <Modal.Header>Organization Details</Modal.Header>
      <Modal.Body>
        <div className="flex flex-col gap-2">
          <Label>Organization Name</Label>
          <TextInput
            name="name"
            onChange={(e) => setForm({ ...form, name: e.currentTarget.value })}
            value={form.name}
            placeholder="WorkPlace LLC"
          />
          <Label>Description</Label>
          <Textarea
            name="description"
            onChange={(e) =>
              setForm({ ...form, description: e.currentTarget.value })
            }
            value={form.description}
            placeholder="Write a bit about your organization..."
            rows={8}
          />
          <div className="mt-2 flex justify-between">
            <Label>Organization Logo</Label>
            <FileManager
              show={showFileManager}
              validMimeTypes={[
                ValidMimeType.PNG,
                ValidMimeType.JPG,
                ValidMimeType.JPEG,
              ]}
              onClose={toggleFileManager}
              multiple={false}
              onSelect={(file) =>
                setForm({ ...form, logo: file?.at(0) || null })
              }
            />
            <Button size="sm" color="pink" outline onClick={toggleFileManager}>
              <TiAttachmentOutline className="size-4" />
            </Button>
          </div>
          <div className="mx-auto flex w-1/3">
            <Image
              src={form.logo?.url || "https://placehold.co/600x400/png"}
              alt="organization logo"
              width={300}
              height={200}
              className="w-full rounded object-cover"
            />
          </div>
        </div>
      </Modal.Body>
      <Modal.Footer className="flex justify-end">
        <Button color="pink" outline onClick={handleSubmit}>
          Save
        </Button>
      </Modal.Footer>
    </Modal>
  );
};
