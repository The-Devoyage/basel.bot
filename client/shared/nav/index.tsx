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
import { addToast } from "../useStore/toast";
import { removeToken } from "../useStore/auth";

export const Nav = () => {
  const themeMode = useThemeMode();
  const windowSize = useWindowSize();
  const {
    store: { token },
    dispatch,
  } = useContext(GlobalContext);

  const handleSignout = async () => {
    try {
      localStorage.removeItem("token");
      dispatch(removeToken());
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

      dispatch(
        addToast({
          type: "success",
          description: "Successfully signed out.",
        }),
      );
    } catch (error) {
      console.error(error);
      dispatch(
        addToast({
          type: "error",
          description: "An error occurred while signing out.",
        }),
      );
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
                myemail@here.com
              </span>
            </Dropdown.Header>
            <Dropdown.Item href="/my-basel">My Basel</Dropdown.Item>
            <Dropdown.Item href="/account">Settings</Dropdown.Item>
            <Dropdown.Item
              onClick={() =>
                themeMode.setMode(themeMode.mode === "dark" ? "light" : "dark")
              }
            >
              {themeMode.mode === "dark" ? "Light Mode" : "Dark Mode"}
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
