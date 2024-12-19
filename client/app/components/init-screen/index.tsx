import { ChatCard } from "@/shared/chat-card";
import {
  BreakBarriers,
  LearnAboutBasel,
  ProfileViews,
  RecruiterWelcome,
} from "./components";

export const InitScreen = () => {
  return (
    <div
      className="mx-auto flex h-full flex-col items-center justify-center space-y-4"
      id="init_screen"
    >
      <RecruiterWelcome />
      <div className="flex w-full flex-col gap-4 md:flex-row">
        <ChatCard
          message={{
            text: `Hello there! I'm Basel, your personal career assistant. I am 
                   ready to help you find jobs, prepare for interviews, and keep 
                   your dynamic resume up to date. **How can I help you today?**`,
            sender: "bot",
            timestamp: new Date(),
          }}
        />
        <ProfileViews />
      </div>
      <LearnAboutBasel />
      <BreakBarriers />
    </div>
  );
};
