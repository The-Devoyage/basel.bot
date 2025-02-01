import {
  BreakBarriers,
  Standup,
  LearnAboutBasel,
  Onboarding,
  ProfileViews,
  RecentInterviews,
  RecruiterWelcome,
  UserWelcome,
  WelcomeMessage,
  ChatNow,
} from "./components";

export const InitScreen = () => {
  return (
    <div className="mx-auto flex h-full flex-col space-y-4">
      <Onboarding />
      <div className="flex w-full flex-col gap-4 md:flex-row">
        <div className="order-2 w-full md:order-1">
          <WelcomeMessage />
        </div>
        <div className="order-1 flex w-full flex-col gap-2 md:order-2 md:w-1/3">
          <div className="space-y-2">
            <UserWelcome />
            <RecruiterWelcome />
          </div>
          <div>
            <ProfileViews />
          </div>
          <ChatNow />
        </div>
      </div>
      <Standup />
      <RecentInterviews />
      <LearnAboutBasel />
      <BreakBarriers />
    </div>
  );
};
