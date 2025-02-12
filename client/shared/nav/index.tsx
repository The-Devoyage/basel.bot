import {
  Avatar,
  Dropdown,
  DropdownDivider,
  DropdownHeader,
  DropdownItem,
  Navbar,
  NavbarBrand,
  NavbarCollapse,
  NavbarLink,
  NavbarToggle,
} from "flowbite-react";
import {
  NotificationToggle,
  SignoutDropdownItem,
  ThemeModeItem,
  UnauthenticatedCta,
} from "./components";
import { BiSolidLeaf } from "react-icons/bi";
import { Endpoint, callApi } from "@/api";

export const Nav = async () => {
  const isAuthenticated = await callApi({
    endpoint: Endpoint.Verify,
    path: null,
    body: null,
    query: null,
  });
  const me = await callApi({
    endpoint: Endpoint.Me,
    path: null,
    body: null,
    query: null,
  });

  return (
    <Navbar
      className="sticky top-0 z-20 shadow-lg shadow-blue-200/50 dark:bg-slate-950 dark:shadow-blue-950/75"
      fluid
    >
      {/*Mobile Nav*/}
      {isAuthenticated.success ? (
        <div className="flex md:hidden">
          <NavbarToggle />
          <NavbarBrand
            href="/"
            className="ml-2 flex items-center space-x-2 text-2xl font-bold dark:text-white md:hidden"
          >
            <BiSolidLeaf className="text-green-400 md:hidden" />
            <span className="text-green-400 md:hidden">basel.bot</span>
          </NavbarBrand>
        </div>
      ) : (
        <NavbarBrand
          href="/"
          className="flex items-center space-x-2 text-2xl font-bold dark:text-white md:hidden"
        >
          <BiSolidLeaf className="text-green-400 md:hidden" />
          <span className="text-green-400 md:hidden">basel.bot</span>
        </NavbarBrand>
      )}
      {/*Desktop Nav*/}
      <div className="flex gap-6">
        <NavbarBrand
          href="/"
          className="flex items-center space-x-2 text-2xl font-bold dark:text-white"
        >
          <BiSolidLeaf className="hidden text-green-400 md:flex" />
          <span className="hidden text-green-400 md:block">basel.bot</span>
        </NavbarBrand>
        <a
          href="/interviews"
          className="hidden self-end text-slate-400 md:flex"
        >
          Interviews
        </a>
      </div>
      {isAuthenticated.success ? (
        <>
          <div className="flex gap-2 md:order-3">
            <NotificationToggle />
            <Dropdown
              arrowIcon={false}
              inline
              label={
                <Avatar
                  alt="User settings"
                  rounded
                  placeholderInitials={me?.data?.first_initial}
                  bordered
                  color="success"
                  img={me?.data?.profile_image?.url}
                  theme={{
                    root: {
                      img: {
                        on: "flex items-center justify-center object-cover",
                      },
                    },
                  }}
                />
              }
            >
              <DropdownHeader>
                <span className="block text-sm">
                  {me?.data?.first_name} {me?.data?.last_name}
                </span>
                <span className="block truncate text-sm font-medium">
                  {me?.data?.email}
                </span>
              </DropdownHeader>
              <DropdownItem href="/my-basel">My Basel</DropdownItem>
              <DropdownItem href="/account">Account</DropdownItem>
              <DropdownItem href="/organizations">Organizations</DropdownItem>
              <ThemeModeItem />
              <DropdownDivider />
              <SignoutDropdownItem />
            </Dropdown>
          </div>
          {/*Mobile Dropdown*/}
          <NavbarCollapse
            style={{ marginBottom: "0.1rem" }}
            className="md:hidden"
          >
            <NavbarLink href="/">Home</NavbarLink>
            <NavbarLink href="/interviews">Interviews</NavbarLink>
          </NavbarCollapse>
        </>
      ) : (
        <UnauthenticatedCta />
      )}
    </Navbar>
  );
};
