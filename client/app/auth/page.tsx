import { Card } from "flowbite-react";
import { AuthForm } from "./components";

const AuthPage = () => {
  return (
    <section className="container mx-auto flex w-full flex-col items-center justify-center space-y-4 p-4">
      <Card>
        <AuthForm />
      </Card>
    </section>
  );
};

export default AuthPage;
