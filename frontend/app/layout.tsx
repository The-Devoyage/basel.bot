import type { Metadata } from "next";
import { Space_Mono } from "next/font/google";
import { ThemeModeScript } from "flowbite-react";
import { GlobalProvider } from "./provider";
import { ChatInput } from "@/shared/chat-input";
import { Nav } from "@/shared/nav";
import "./globals.css";

const spaceMono = Space_Mono({
  weight: "400",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Basels",
  description: "Basel's here to help you find and watch products and services.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" id="root" className="scroll-smooth">
      <head>
        <ThemeModeScript />
      </head>
      <GlobalProvider>
        <body className={`h-screen w-full bg-slate-100 ${spaceMono.className}`}>
          <Nav />
          <main
            className="container relative top-16 mx-auto mb-16 flex p-4 dark:bg-slate-800"
            style={{
              minHeight: "calc(100vh - 148px)",
            }}
          >
            {children}
          </main>
          <footer className="sticky bottom-0 w-full border-t bg-white dark:border-green-500 dark:bg-slate-900">
            <ChatInput />
          </footer>
        </body>
      </GlobalProvider>
    </html>
  );
}
