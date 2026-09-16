import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";

import { Navbar } from "@/components/Navbar";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "PharmaIntel — Pharma Market Intelligence Agent",
  description:
    "AI-powered pharmaceutical market intelligence: web-researched market briefs and structured earnings analysis.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="flex min-h-full flex-col">
        <Navbar />
        {children}
        <footer className="border-t border-zinc-200/80 py-8">
          <div className="mx-auto w-full max-w-6xl px-4 text-sm text-zinc-400 sm:px-6">
            PharmaIntel — AI-powered pharmaceutical market intelligence.
          </div>
        </footer>
      </body>
    </html>
  );
}