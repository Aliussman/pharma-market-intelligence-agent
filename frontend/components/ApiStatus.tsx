"use client";

import { useEffect, useState } from "react";
import { Wifi, WifiOff } from "lucide-react";

import { API_URL } from "@/lib/api";

export function ApiStatus() {
  const [online, setOnline] = useState<boolean | null>(null);

  useEffect(() => {
    let cancelled = false;
    fetch(`${API_URL}/`)
      .then((r) => r.ok)
      .then((ok) => {
        if (!cancelled) setOnline(ok);
      })
      .catch(() => {
        if (!cancelled) setOnline(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const label =
    online === null ? "Checking API…" : online ? "API online" : "API offline";

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium ${
        online === null
          ? "bg-zinc-100 text-zinc-500"
          : online
            ? "bg-emerald-50 text-emerald-700"
            : "bg-red-50 text-red-700"
      }`}
    >
      {online === null ? (
        <Wifi className="size-3.5 animate-pulse" />
      ) : online ? (
        <Wifi className="size-3.5" />
      ) : (
        <WifiOff className="size-3.5" />
      )}
      {label}
    </span>
  );
}