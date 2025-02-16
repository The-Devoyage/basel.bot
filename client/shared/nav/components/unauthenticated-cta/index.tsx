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
            <Navbar.Link href="/">Home</Navbar.Link>
            <Navbar.Link href="/interviews">Interviews</Navbar.Link>
            <Navbar.Link href="/chat">Chat</Navbar.Link>
            <Navbar.Link
              href="#"
              onClick={() =>
                themeMode.setMode(themeMode.mode === "dark" ? "light" : "dark")
              }
            >
              {themeMode.mode === "dark" ? "Light" : "Dark"}
            </Navbar.Link>
            <AuthButton isButton={false} />
          </Navbar.Collapse>
        </>
      ) : (
        <div className="flex">
          <DarkThemeToggle className="mr-2" />
          <div className="flex flex-row">
            <AuthButton isButton />
          </div>
        </div>
      )}
    </>
  );
};
