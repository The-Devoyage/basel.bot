"use client";

import {
  Avatar,
  DarkThemeToggle,
  Dropdown,
  Navbar,
  useThemeMode,
} from "flowbite-react";
import Logo from "../../public/logo.svg";
import { useContext, useEffect, useState } from "react";
import { useWindowSize } from "../useWindowSize";
import { Auth } from "./components";
import { GlobalContext } from "@/app/provider";

export const Nav = () => {
  const themeMode = useThemeMode();
  const [fill, setFill] = useState("#0E9F6E");
  const windowSize = useWindowSize();
  const { token } = useContext(GlobalContext);

  useEffect(() => {
    setFill(themeMode.mode === "dark" ? "#31C48D" : "#0E9F6E");
  }, [themeMode]);

  return (
    <Navbar className="fixed left-0 right-0 top-0 z-10 border-b dark:bg-slate-950">
      <Navbar.Brand href="/" className="text-2xl font-bold dark:text-white">
        <Logo style={{ fill, height: "3rem" }} />
      </Navbar.Brand>
      <Navbar.Toggle />
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
            <Dropdown.Item
              onClick={() => {
                window.localStorage.removeItem("token");
                window.location.reload();
              }}
            >
              Sign out
            </Dropdown.Item>
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
              <Auth />
            </Navbar.Collapse>
          ) : (
            <div className="flex">
              <DarkThemeToggle className="mr-2" />
              <div className="flex flex-row">
                <Auth />
              </div>
            </div>
          )}
        </>
      )}
    </Navbar>
  );
};
