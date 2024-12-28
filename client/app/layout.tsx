import type { Metadata } from "next";
import { Space_Mono } from "next/font/google";
import { ThemeModeScript } from "flowbite-react";
import { GlobalProvider } from "./provider";
import { ChatInput } from "@/shared/chat-input";
import { Nav } from "@/shared/nav";
import { Toaster } from "@/shared/toaster";
import "./globals.css";
import { Suspense } from "react";
import { Loader } from "@/shared/loader";

const spaceMono = Space_Mono({
  weight: "400",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Basel",
  description:
    "Basel is your virtual professional you. Your probot (professional robot) is here to stand in your place for initial interviews and screenings. Drop a link and let the recuriter talk to your bot.",
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" id="root" className="scroll-smooth">
      <head>
        <link rel="icon" href="/logo.svg" sizes="any" />
        <meta
          name="viewport"
          content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0, viewport-fit=cover"
        />

        <ThemeModeScript />
      </head>
      <body
        className={`h-screen w-full bg-slate-100 dark:bg-slate-900 ${spaceMono.className}`}
      >
        <Suspense
          fallback={
            <Loader message="Your next interview just got much easier." />
          }
        >
          <GlobalProvider>
            <Toaster />
            <Nav />
            <main
              className="container relative top-16 mx-auto mb-16 flex p-4 dark:bg-slate-900"
              style={{
                minHeight: "calc(100vh - 148px)",
              }}
            >
              {children}
            </main>
            <footer className="sticky bottom-0 w-full border-t bg-white dark:border-slate-500 dark:bg-slate-950">
              <ChatInput />
            </footer>
          </GlobalProvider>
        </Suspense>
      </body>
    </html>
  );
}
