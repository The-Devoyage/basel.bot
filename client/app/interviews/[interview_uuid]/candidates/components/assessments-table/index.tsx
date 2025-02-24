import { InterviewAssesment } from "@/types/interview_assessment";
import {
  Avatar,
  Rating,
  RatingStar,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeadCell,
  TableRow,
} from "flowbite-react";
import { FC } from "react";

export const AssessmentsTable: FC<{
  interviewAssessments: InterviewAssesment[];
}> = ({ interviewAssessments }) => (
  <Table>
    <TableHead>
      <TableHeadCell />
      <TableHeadCell className="text-center">Candidate</TableHeadCell>
      <TableHeadCell className="text-center">Overall Rating</TableHeadCell>
      <TableHeadCell className="hidden text-center md:table-cell">
        Content/Relevance
      </TableHeadCell>
      <TableHeadCell className="hidden text-center md:table-cell">
        Communication
      </TableHeadCell>
      <TableHeadCell className="hidden text-center md:table-cell">
        Delivery
      </TableHeadCell>
      <TableHeadCell className="hidden text-center md:table-cell">
        Structure
      </TableHeadCell>
      <TableHeadCell className="hidden text-center md:table-cell">
        Adaptability
      </TableHeadCell>
      <TableHeadCell className="hidden text-center md:table-cell">
        Industry Knowledge
      </TableHeadCell>
    </TableHead>
    <TableBody>
      {interviewAssessments.map((ia) => (
        <TableRow key={ia.uuid}>
          <TableCell>
            <Avatar
              rounded
              img={ia.user.profile_image?.url}
              placeholderInitials={ia.user.first_initial}
              bordered
              color="success"
              theme={{
                root: {
                  img: {
                    on: "flex items-center justify-center object-cover",
                  },
                },
              }}
            />
          </TableCell>
          <TableCell className="text-center">{ia.user.full_name}</TableCell>
          <TableCell>
            <div className="flex items-center justify-center">
              <Rating>
                {Array.from({ length: ia.overall }, (_, i) => (
                  <RatingStar key={i} />
                ))}
                {Array.from({ length: 5 - ia.overall }, (_, i) => (
                  <RatingStar key={i} filled={false} />
                ))}
              </Rating>
            </div>
          </TableCell>
          <TableCell className="hidden text-center md:table-cell">
            {ia.content_relevance}
          </TableCell>
          <TableCell className="hidden text-center md:table-cell">
            {ia.communication_skills}
          </TableCell>
          <TableCell className="hidden text-center md:table-cell">
            {ia.confidence_delivery}
          </TableCell>
          <TableCell className="hidden text-center md:table-cell">
            {ia.structure_organization}
          </TableCell>
          <TableCell className="hidden text-center md:table-cell">
            {ia.adaptability_critical_thinking}
          </TableCell>
          <TableCell className="hidden text-center md:table-cell">
            {ia.technical_industry_knowledge}
          </TableCell>
        </TableRow>
      ))}
    </TableBody>
  </Table>
);
