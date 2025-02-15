"use client";

import { Endpoint } from "@/api";
import { useCallApi } from "@/shared/useCallApi";
import {
  Dispatch,
  FC,
  SetStateAction,
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import { Organization, File } from "@/types";
import { GlobalContext } from "../provider";
import { addToast } from "@/shared/useStore/toast";
import { usePagination } from "@/shared/usePagination";

export interface OrganizationForm {
  uuid?: string;
  name: string;
  description: string;
  logo: File | null;
}

interface OrganizationsPageContext {
  organizations: Organization[];
  loading: boolean;
  showEditOrganizationModal: boolean;
  handleCreateOrganization: (
    form: OrganizationForm,
    callback: () => void,
  ) => void;
  handleUpdateOrganization: (
    form: OrganizationForm,
    callback: () => void,
  ) => void;
  toggleEditOrganizationModal: () => void;
  pager: ReturnType<typeof usePagination> | null;
  selectedOrganization: Organization | null;
  setSelectedOrganization: Dispatch<SetStateAction<Organization | null>>;
}

export const OrganizationsPageContext = createContext<OrganizationsPageContext>(
  {
    organizations: [],
    loading: false,
    showEditOrganizationModal: false,
    handleCreateOrganization: () => Promise.resolve(),
    handleUpdateOrganization: () => Promise.resolve(),
    toggleEditOrganizationModal: () => null,
    pager: null,
    selectedOrganization: null,
    setSelectedOrganization: () => null,
  },
);

export const OrganizationsPageProvider: FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [showEditOrganizationModal, setShowEditOrganizationModal] =
    useState(false);
  const { dispatch } = useContext(GlobalContext);
  const pager = usePagination();
  const [selectedOrganization, setSelectedOrganization] =
    useState<Organization | null>(null);

  const {
    res,
    loading,
    call: fetchOrganizations,
  } = useCallApi(
    {
      endpoint: Endpoint.GetOrganizations,
      query: {
        my_organizations: true,
        limit: pager.pagination.limit,
        offset: pager.nextOffset,
      },
      body: null,
      path: null,
    },
    {
      callOnMount: true,
      onSuccess: (res) => {
        pager.handleSetTotal(res?.total);
      },
    },
  );
  const organizations = useMemo(() => res?.data || [], [res?.data]);
  const { call: createOrganization } = useCallApi(
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
        setShowEditOrganizationModal(false);
        await fetchOrganizations();
      },
    },
  );
  const { call: updateOrganization } = useCallApi(
    {
      endpoint: Endpoint.UpdateOrganization,
      method: "PATCH",
      body: {
        uuid: "",
        description: "",
        name: "",
      },
      path: null,
      query: null,
    },
    {
      onSuccess: async () => {
        dispatch(
          addToast({ type: "success", description: "Organization Updated" }),
        );
        setShowEditOrganizationModal(false);
        await fetchOrganizations();
      },
    },
  );

  useEffect(() => {
    fetchOrganizations();
  }, [pager.pagination.currentPage]);

  const handleUpdateOrganization =
    () => async (form: OrganizationForm, callback: () => void) => {
      const res = await updateOrganization({
        body: {
          uuid: form.uuid!,
          name: form.name,
          description: form.description,
          logo: form.logo || undefined,
        },
        path: null,
        query: null,
      });
      if (res?.success) callback();
    };

  const handleCreateOrganization =
    () => async (form: OrganizationForm, callback: () => void) => {
      const res = await createOrganization({
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

  const toggleEditOrganizationModal = useCallback(
    () => () => {
      setShowEditOrganizationModal(!showEditOrganizationModal);
    },
    [showEditOrganizationModal],
  );

  const value = useMemo(
    () => ({
      organizations,
      loading,
      showEditOrganizationModal,
      handleCreateOrganization,
      toggleEditOrganizationModal,
      pager,
      selectedOrganization,
      setSelectedOrganization,
      handleUpdateOrganization,
    }),
    [
      organizations,
      loading,
      showEditOrganizationModal,
      pager,
      selectedOrganization,
      handleCreateOrganization,
      handleUpdateOrganization,
      toggleEditOrganizationModal,
    ],
  );

  return (
    <OrganizationsPageContext.Provider value={value}>
      {children}
    </OrganizationsPageContext.Provider>
  );
};
