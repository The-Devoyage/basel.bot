"use client";

import { Dropdown, useThemeMode } from "flowbite-react";

export const ThemeModeItem = () => {
  const themeMode = useThemeMode();
  return (
    <Dropdown.Item
      onClick={() =>
        themeMode.setMode(themeMode.mode === "dark" ? "light" : "dark")
      }
    >
      {themeMode.mode === "dark" ? "Light Mode" : "Dark Mode"}
    </Dropdown.Item>
  );
};
