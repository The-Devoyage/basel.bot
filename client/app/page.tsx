import { ChatBody, InitScreen } from "./components";
import LogRocket from "logrocket";
LogRocket.init("sqlyqw/basel");

export default function Home() {
  return (
    <section className="min-w-75 flex w-full flex-col space-y-4">
      <InitScreen />
      <ChatBody />
    </section>
  );
}
