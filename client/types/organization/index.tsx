import { File, User } from "@/types";

export interface Organization {
  uuid: string;
  name: string;
  description: string;
  logo?: File;
  slug: string;
  status: boolean;
  created_at: Date;
  users: OrganizationUser[];
}

export interface OrganizationUser {
  uuid: string;
  user: User;
  organization: Organization;
  status: boolean;
}
