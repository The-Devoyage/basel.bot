import { ChatCard } from "@/shared/chat-card";
import {
  BreakBarriers,
  Standup,
  LearnAboutBasel,
  Onboarding,
  ProfileViews,
  RecentInterviews,
  RecruiterWelcome,
  UserWelcome,
} from "./components";
import { message } from "./message";

export const InitScreen = () => {
  return (
    <div
      className="mx-auto flex h-full flex-col items-center justify-center space-y-4"
      id="init_screen"
    >
      <Onboarding />
      <RecruiterWelcome />
      <div className="flex w-full flex-col gap-4 md:flex-row">
        <ChatCard
          message={{
            text: message,
            sender: "bot",
            timestamp: new Date(),
          }}
        />
        <div className="flex flex-col gap-2">
          <div>
            <UserWelcome />
          </div>
          <div>
            <ProfileViews />
          </div>
        </div>
      </div>
      <Standup />
      <RecentInterviews />
      <LearnAboutBasel />
      <BreakBarriers />
    </div>
  );
};
