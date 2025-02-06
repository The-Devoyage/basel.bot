"use client";

import { Endpoint } from "@/api";
import { useCallApi } from "@/shared/useCallApi";
import { FC, createContext, useContext, useMemo, useState } from "react";
import { Organization, File } from "@/types";
import { GlobalContext } from "../provider";
import { addToast } from "@/shared/useStore/toast";

export interface OrganizationForm {
  name: string;
  description: string;
  logo: File | null;
}

interface OrganizationsPageContext {
  organizations: Organization[];
  loading: boolean;
  showCreateOrganizationModal: boolean;
  handleCreateOrganization: (
    form: OrganizationForm,
    callback: () => void,
  ) => Promise<void>;
  toggleCreateOrganizationModal: () => void;
}

export const OrganizationsPageContext = createContext<OrganizationsPageContext>(
  {
    organizations: [],
    loading: false,
    showCreateOrganizationModal: false,
    handleCreateOrganization: () => Promise.resolve(),
    toggleCreateOrganizationModal: () => null,
  },
);

export const OrganizationsPageProvider: FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [showCreateOrganizationModal, setShowCreateOrganizationModal] =
    useState(false);
  const { dispatch } = useContext(GlobalContext);
  const {
    res,
    loading,
    call: fetchOrganizations,
  } = useCallApi(
    {
      endpoint: Endpoint.GetOrganizations,
      query: { my_organizations: true },
      body: null,
      path: null,
    },
    {
      callOnMount: true,
    },
  );
  const organizations = res?.data || [];
  const { call } = useCallApi(
    {
      endpoint: Endpoint.CreateOrganization,
      method: "POST",
      body: {
        description: "",
        name: "",
      },
      path: null,
      query: null,
    },
    {
      onSuccess: async () => {
        dispatch(
          addToast({ type: "success", description: "Organization Created" }),
        );
        setShowCreateOrganizationModal(false);
        await fetchOrganizations();
      },
    },
  );

  const handleCreateOrganization = async (
    form: OrganizationForm,
    callback: () => void,
  ) => {
    const res = await call({
      body: {
        name: form.name,
        description: form.description,
        logo: form.logo || undefined,
      },
      path: null,
      query: null,
    });

    if (res?.success) callback();
  };

  const toggleCreateOrganizationModal = () => {
    setShowCreateOrganizationModal(!showCreateOrganizationModal);
  };

  const value = useMemo(
    () => ({
      organizations,
      loading,
      showCreateOrganizationModal,
      handleCreateOrganization,
      toggleCreateOrganizationModal,
    }),
    [organizations, loading, showCreateOrganizationModal],
  );

  return (
    <OrganizationsPageContext.Provider value={value}>
      {children}
    </OrganizationsPageContext.Provider>
  );
};
