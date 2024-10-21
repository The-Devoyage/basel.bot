"use client";

import {
  Avatar,
  DarkThemeToggle,
  Dropdown,
  Navbar,
  useThemeMode,
} from "flowbite-react";
import { useContext } from "react";
import { useWindowSize } from "../useWindowSize";
import { AuthButton } from "./components";
import { GlobalContext } from "@/app/provider";
import { BiSolidLeaf } from "react-icons/bi";
import { v4 } from "uuid";

export const Nav = () => {
  const themeMode = useThemeMode();
  const windowSize = useWindowSize();
  const { token, setToken, dispatch } = useContext(GlobalContext);

  const handleSignout = async () => {
    try {
      localStorage.removeItem("token");
      setToken?.(null);
      const res = await fetch("http://localhost:8000/logout", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          ContentType: "application/json",
        },
      });
      const data = await res.json();

      if (!data.success) {
        throw new Error(data.error || data.detail);
      }

      dispatch?.({
        type: "ADD_TOAST",
        payload: {
          uuid: v4(),
          type: "success",
          description: "Successfully signed out.",
        },
      });
    } catch (error) {
      console.error(error);
      dispatch?.({
        type: "ADD_TOAST",
        payload: {
          uuid: v4(),
          type: "error",
          description: "An error occurred while signing out.",
        },
      });
    }
  };

  return (
    <Navbar className="fixed left-0 right-0 top-0 z-10 border-b dark:bg-slate-950">
      <Navbar.Brand
        href="/"
        className="space-x-2 text-2xl font-bold dark:text-white"
      >
        <BiSolidLeaf className="text-green-400" />
        <span className="text-green-400">basel.bot</span>
      </Navbar.Brand>
      {token ? (
        <div className="flex md:order-2">
          <Dropdown
            arrowIcon={false}
            inline
            label={
              <Avatar
                alt="User settings"
                img="https://flowbite.com/docs/images/people/profile-picture-5.jpg"
                rounded
              />
            }
          >
            <Dropdown.Header>
              <span className="block text-sm">Bonnie Green</span>
              <span className="block truncate text-sm font-medium">
                name@flowbite.com
              </span>
            </Dropdown.Header>
            <Dropdown.Item>Dashboard</Dropdown.Item>
            <Dropdown.Item>Settings</Dropdown.Item>
            <Dropdown.Item
              onClick={() =>
                themeMode.setMode(themeMode.mode === "dark" ? "light" : "dark")
              }
            >
              {themeMode.mode === "dark" ? "Light" : "Dark"}
            </Dropdown.Item>
            <Dropdown.Divider />
            <Dropdown.Item onClick={handleSignout}>Sign out</Dropdown.Item>
          </Dropdown>
        </div>
      ) : (
        <>
          {windowSize.isMobile ? (
            <Navbar.Collapse>
              <Navbar.Link
                href="#"
                onClick={() =>
                  themeMode.setMode(
                    themeMode.mode === "dark" ? "light" : "dark",
                  )
                }
              >
                {themeMode.mode === "dark" ? "Light" : "Dark"}
              </Navbar.Link>
              <AuthButton />
            </Navbar.Collapse>
          ) : (
            <div className="flex">
              <DarkThemeToggle className="mr-2" />
              <div className="flex flex-row">
                <AuthButton />
              </div>
            </div>
          )}
        </>
      )}
    </Navbar>
  );
};
