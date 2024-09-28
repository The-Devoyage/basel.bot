"use client";

import { DarkThemeToggle, Navbar, useThemeMode } from "flowbite-react";
import Logo from "../../public/logo.svg";
import { useEffect, useState } from "react";
import { useWindowSize } from "../useWindowSize";

export const Nav = () => {
  const themeMode = useThemeMode();
  const [fill, setFill] = useState("#0E9F6E");
  const windowSize = useWindowSize();

  useEffect(() => {
    setFill(themeMode.mode === "dark" ? "#31C48D" : "#0E9F6E");
  }, [themeMode]);

  return (
    <Navbar className="fixed left-0 right-0 top-0 z-10 border-b dark:bg-slate-900">
      <Navbar.Brand href="/" className="text-2xl font-bold dark:text-white">
        <Logo style={{ fill, height: "3rem" }} />
      </Navbar.Brand>
      <Navbar.Toggle />
      <Navbar.Collapse>
        <Navbar.Link href="#">Search</Navbar.Link>
        <Navbar.Link href="#">Watching</Navbar.Link>
        <Navbar.Link href="#">Cart</Navbar.Link>
        {windowSize.isMobile && (
          <Navbar.Link
            onClick={() =>
              themeMode.setMode(themeMode.mode === "dark" ? "light" : "dark")
            }
          >
            {themeMode.mode === "dark" ? "Light" : "Dark"}
          </Navbar.Link>
        )}
      </Navbar.Collapse>
      <DarkThemeToggle className="hidden md:block" />
    </Navbar>
  );
};
