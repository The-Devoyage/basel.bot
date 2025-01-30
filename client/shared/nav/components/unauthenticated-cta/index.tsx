"use client";

import { DarkThemeToggle, Navbar, useThemeMode } from "flowbite-react";
import { useWindowSize } from "../../../useWindowSize";
import { AuthButton } from "@/shared/auth-button";

export const UnauthenticatedCta = () => {
  const windowSize = useWindowSize();
  const themeMode = useThemeMode();

  return (
    <>
      {windowSize.isMobile ? (
        <>
          <Navbar.Toggle />
          <Navbar.Collapse>
            <Navbar.Link
              href="#"
              onClick={() =>
                themeMode.setMode(themeMode.mode === "dark" ? "light" : "dark")
              }
            >
              {themeMode.mode === "dark" ? "Light" : "Dark"}
            </Navbar.Link>
            <AuthButton />
          </Navbar.Collapse>
        </>
      ) : (
        <div className="flex">
          <DarkThemeToggle className="mr-2" />
          <div className="flex flex-row">
            <AuthButton />
          </div>
        </div>
      )}
    </>
  );
};
