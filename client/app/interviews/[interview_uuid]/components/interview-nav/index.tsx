"use client";

import { ListGroup, ListGroupItem } from "flowbite-react";
import { useContext } from "react";
import { InterviewPageContext } from "../../context";

export const InterviewNav = () => {
  const { interview, organizations } = useContext(InterviewPageContext);

  if (!interview) return null;

  const items = [
    { href: `/interviews/${interview.uuid}`, label: "Interview" },
    {
      href: `/interviews/${interview.uuid}/candidates`,
      label: "Candidates",
      requireOrganization: true,
    },
    {
      label: "Questions",
      href: `/interviews/${interview.uuid}/questions`,
    },
  ].filter((i) => {
    if (i.requireOrganization) {
      return (
        organizations?.findIndex(
          (o) => interview.organization?.uuid === o.uuid,
        ) > -1
      );
    }
    return true;
  });

  return (
    <ListGroup className="w-full md:w-auto">
      {items.map((i, index) => (
        <ListGroupItem key={index} href={i.href}>
          {i.label}
        </ListGroupItem>
      ))}
    </ListGroup>
  );
};
