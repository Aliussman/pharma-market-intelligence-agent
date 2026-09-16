import { Pill } from "lucide-react";

import { ApiStatus } from "@/components/ApiStatus";

const links = [
  { href: "#market-brief", label: "Market Brief" },
  { href: "#analyzer", label: "Analyzer" },
];

export function Navbar() {
  return (
    <header className="sticky top-0 z-50 border-b border-zinc-200/80 bg-white/80 backdrop-blur-md">
      <nav className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4 sm:px-6">
        <div className="flex items-center gap-2">
          <span className="flex size-8 items-center justify-center rounded-lg bg-emerald-600 text-white shadow-sm">
            <Pill className="size-4.5" />
          </span>
          <span className="text-sm font-semibold tracking-tight text-zinc-900">
            Pharma<span className="text-emerald-600">Intel</span>
          </span>
        </div>

        <div className="hidden items-center gap-6 text-sm font-medium text-zinc-600 sm:flex">
          {links.map((link) => (
            <a key={link.href} href={link.href} className="transition-colors hover:text-zinc-900">
              {link.label}
            </a>
          ))}
        </div>

        <ApiStatus />
      </nav>
    </header>
  );
}