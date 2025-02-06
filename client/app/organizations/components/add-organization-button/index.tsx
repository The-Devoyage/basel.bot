"use client";

import { Button, Label, Modal, TextInput, Textarea } from "flowbite-react";
import { useContext, useState } from "react";
import { BsPlusLg } from "react-icons/bs";
import Image from "next/image";
import { TiAttachmentOutline } from "react-icons/ti";
import { FileManager } from "@/shared/file-manager";
import { OrganizationForm, OrganizationsPageContext } from "../../context";

const initialForm: OrganizationForm = {
  name: "",
  description: "",
  logo: null,
};

export const AddOrganizationButton = () => {
  const {
    showCreateOrganizationModal,
    toggleCreateOrganizationModal,
    handleCreateOrganization,
  } = useContext(OrganizationsPageContext);
  const [showFileManager, setShowFileManager] = useState(false);
  const [form, setForm] = useState<OrganizationForm>(initialForm);

  const toggleFileManager = () => {
    setShowFileManager(!showFileManager);
  };

  const handleSubmit = async () => {
    await handleCreateOrganization(form, () => setForm(initialForm));
  };

  return (
    <>
      <Modal
        show={showCreateOrganizationModal}
        onClose={toggleCreateOrganizationModal}
      >
        <Modal.Header>Organization Details</Modal.Header>
        <Modal.Body>
          <div className="flex flex-col gap-2">
            <Label>Organization Name</Label>
            <TextInput
              name="name"
              onChange={(e) =>
                setForm({ ...form, name: e.currentTarget.value })
              }
              value={form.name}
            />
            <Label>Description</Label>
            <Textarea
              name="description"
              onChange={(e) =>
                setForm({ ...form, description: e.currentTarget.value })
              }
            />
            <div className="mt-2 flex justify-between">
              <Label>Organization Logo</Label>
              <FileManager
                show={showFileManager}
                onClose={toggleFileManager}
                multiple={false}
                onSelect={(file) =>
                  setForm({ ...form, logo: file?.at(0) || null })
                }
              />
              <Button
                size="sm"
                color="pink"
                outline
                onClick={toggleFileManager}
              >
                <TiAttachmentOutline className="h-4 w-4" />
              </Button>
            </div>
            <Image
              src={form.logo?.url || "https://placehold.co/600x400/png"}
              alt="organization logo"
              width={300}
              height={200}
              className="w-full rounded object-cover"
            />
          </div>
        </Modal.Body>
        <Modal.Footer className="flex justify-end">
          <Button color="pink" outline onClick={handleSubmit}>
            Save
          </Button>
        </Modal.Footer>
      </Modal>
      <Button
        outline
        gradientMonochrome="pink"
        onClick={toggleCreateOrganizationModal}
      >
        <BsPlusLg className="h-4 w-4" />
      </Button>
    </>
  );
};
