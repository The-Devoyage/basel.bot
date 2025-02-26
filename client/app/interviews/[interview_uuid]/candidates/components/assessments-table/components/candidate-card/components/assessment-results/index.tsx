"use client";

import { InterviewAssesment } from "@/types/interview_assessment";
import {
  Accordion,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeadCell,
  TableRow,
} from "flowbite-react";
import { FC } from "react";

export const AssessmentResults: FC<{
  interviewAssessment: InterviewAssesment;
}> = ({ interviewAssessment }) => {
  return (
    <Accordion collapseAll>
      <Accordion.Panel>
        <Accordion.Title>Results</Accordion.Title>
        <Accordion.Content>
          <Table>
            <TableHead>
              <TableHeadCell>Category</TableHeadCell>
              <TableHeadCell className="text-center">Score</TableHeadCell>
            </TableHead>
            <TableBody>
              <TableRow>
                <TableCell>Content</TableCell>
                <TableCell className="text-center">
                  {interviewAssessment.content_relevance}
                </TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Communication</TableCell>
                <TableCell className="text-center">
                  {interviewAssessment.communication_skills}
                </TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Delivery</TableCell>
                <TableCell className="text-center">
                  {interviewAssessment.confidence_delivery}
                </TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Structure</TableCell>
                <TableCell className="text-center">
                  {interviewAssessment.structure_organization}
                </TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Adaptability</TableCell>
                <TableCell className="text-center">
                  {interviewAssessment.adaptability_critical_thinking}
                </TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Technical Knowledge</TableCell>
                <TableCell className="text-center">
                  {interviewAssessment.technical_industry_knowledge}
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </Accordion.Content>
      </Accordion.Panel>
    </Accordion>
  );
};
