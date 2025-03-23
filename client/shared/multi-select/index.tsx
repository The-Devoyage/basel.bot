"use client";

import { Badge, Dropdown } from "flowbite-react";
import { FC } from "react";
import { BiChevronDown } from "react-icons/bi";
import { FaX } from "react-icons/fa6";

interface MultiSelectProps {
  options: { label: string; value: string }[];
  value?: string[];
  onChange?: (selected: string) => void;
}

export const MultiSelect: FC<MultiSelectProps> = ({
  options,
  value = [],
  onChange,
}) => {
  const remaining = options.filter(
    (o) => value.findIndex((v) => v === o.value) === -1,
  );
  const selected = options.filter(
    (o) => value?.findIndex((v) => v === o.value) >= 0,
  );

  return (
    <Dropdown
      dismissOnClick={false}
      renderTrigger={() => (
        <div className="flex w-full cursor-pointer justify-between rounded-lg border-2 bg-slate-50 p-2 dark:border-slate-600 dark:bg-transparent">
          <div className="flex flex-1 flex-wrap gap-2">
            {selected.length ? (
              selected.map((o) => (
                <Badge
                  key={o.value}
                  onClick={(e) => {
                    e.stopPropagation();
                    onChange?.(o.value);
                  }}
                  className="cursor-pointer"
                  color="green"
                >
                  <div className="flex items-center space-x-1">
                    <span>{o.label}</span>
                    <FaX />
                  </div>
                </Badge>
              ))
            ) : (
              <span className="text-sm dark:text-slate-400">
                Select Options
              </span>
            )}
          </div>
          <BiChevronDown className="ml-2 h-4 w-4 self-center dark:text-white" />
        </div>
      )}
      theme={{
        content: "dark:bg-slate-800",
      }}
    >
      {remaining.length ? (
        remaining.map((o) => (
          <Dropdown.Item
            key={o.value}
            onClick={() => onChange?.(o.value)}
            className="text-left"
          >
            {o.label}
          </Dropdown.Item>
        ))
      ) : (
        <Dropdown.Item>No More Options</Dropdown.Item>
      )}
    </Dropdown>
  );
};
