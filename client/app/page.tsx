import { ChatBody, InitScreen } from "./components";

export default function Home() {
  return (
    <section className="min-w-75 flex w-full flex-col space-y-4">
      <InitScreen />
      <ChatBody />
    </section>
  );
}
