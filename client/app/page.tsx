import { InitScreen } from "./components";
// import LogRocket from "logrocket";
// LogRocket.init("sqlyqw/basel");

export default function Home() {
  return (
    <section className="min-w-75 container mx-auto flex w-full flex-col p-4">
      <InitScreen />
    </section>
  );
}
