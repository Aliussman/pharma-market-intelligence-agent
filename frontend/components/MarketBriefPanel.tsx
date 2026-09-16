"use client";

import { useCallback, useEffect, useState } from "react";
import {
  Bot,
  ExternalLink,
  Newspaper,
  RefreshCw,
  Search,
} from "lucide-react";

import { ApiError, getMarketBrief } from "@/lib/api";
import type { MarketBrief } from "@/lib/types";

type BriefState =
  | { status: "loading" }
  | { status: "error"; message: string }
  | { status: "ready"; brief: MarketBrief };

export function MarketBriefPanel() {
  const [topic, setTopic] = useState("pharmaceutical industry");
  const [input, setInput] = useState(topic);
  const [state, setState] = useState<BriefState>({ status: "loading" });

  const runResearch = useCallback(async (value: string) => {
    setState({ status: "loading" });
    try {
      const brief = await getMarketBrief(value);
      setState({ status: "ready", brief });
    } catch (err) {
      const message =
        err instanceof ApiError ? err.message : "Could not reach the backend API.";
      setState({ status: "error", message });
    }
  }, []);

  useEffect(() => {
    let active = true;
    getMarketBrief(topic)
      .then((brief) => {
        if (active) setState({ status: "ready", brief });
      })
      .catch((err) => {
        if (!active) return;
        const message =
          err instanceof ApiError ? err.message : "Could not reach the backend API.";
        setState({ status: "error", message });
      });
    return () => {
      active = false;
    };
  }, [topic]);

  return (
    <section id="market-brief" className="mx-auto w-full max-w-6xl px-4 py-14 sm:px-6">
      <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <div className="mb-2 flex items-center gap-2 text-sm font-semibold uppercase tracking-wider text-emerald-600">
            <Bot className="size-4" /> Autonomous Research Agent
          </div>
          <h2 className="text-2xl font-bold tracking-tight text-zinc-900 sm:text-3xl">
            Pharma Market Brief
          </h2>
          <p className="mt-1 text-zinc-500">
            The agent scans the web and condenses the latest pharma news into a briefing.
          </p>
        </div>
        <form
          className="flex w-full gap-2 sm:w-auto"
          onSubmit={(e) => {
            e.preventDefault();
            const value = input.trim() || "pharmaceutical industry";
            setTopic(value);
          }}
        >
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="e.g. obesity drugs, oncology pipeline…"
            className="h-10 min-w-0 flex-1 rounded-lg border border-zinc-300 bg-white px-3 text-sm text-zinc-900 shadow-sm outline-none transition focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/30 sm:w-72"
          />
          <button
            type="submit"
            className="inline-flex h-10 items-center gap-1.5 rounded-lg bg-zinc-900 px-4 text-sm font-medium text-white shadow-sm transition hover:bg-zinc-700"
          >
            <Search className="size-4" /> Research
          </button>
        </form>
      </div>

      {state.status === "loading" && <BriefSkeleton />}

      {state.status === "error" && (
        <div className="rounded-2xl border border-red-200 bg-red-50 p-6 text-red-700">
          <p className="font-medium">Failed to load the market brief</p>
          <p className="mt-1 text-sm text-red-600">{state.message}</p>
          <button
            onClick={() => runResearch(topic)}
            className="mt-3 inline-flex items-center gap-1.5 rounded-lg bg-red-600 px-3 py-1.5 text-sm font-medium text-white transition hover:bg-red-500"
          >
            <RefreshCw className="size-3.5" /> Retry
          </button>
        </div>
      )}

      {state.status === "ready" && <BriefContent state={state} onRefresh={() => runResearch(topic)} />}
    </section>
  );
}

function BriefContent({
  state,
  onRefresh,
}: {
  state: Extract<BriefState, { status: "ready" }>;
  onRefresh: () => void;
}) {
  const { brief } = state;
  const generatedAt = new Date(brief.generated_at).toLocaleString();

  return (
    <div className="grid gap-6 lg:grid-cols-5">
      <div className="rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm lg:col-span-2">
        <div className="mb-3 flex items-center justify-between">
          <h3 className="text-sm font-semibold uppercase tracking-wider text-zinc-500">
            Executive Overview
          </h3>
          <span className="rounded-full bg-emerald-50 px-2 py-0.5 text-xs font-medium text-emerald-700">
            {brief.topic}
          </span>
        </div>
        <p className="whitespace-pre-wrap leading-relaxed text-zinc-700">
          {brief.market_overview}
        </p>
        <div className="mt-4 flex items-center gap-1.5 text-xs text-zinc-400">
          <span className="size-1.5 rounded-full bg-emerald-500" />
          Generated at {generatedAt}
        </div>
      </div>

      <div className="rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm lg:col-span-3">
        <div className="mb-4 flex items-center justify-between">
          <h3 className="flex items-center gap-2 text-sm font-semibold uppercase tracking-wider text-zinc-500">
            <Newspaper className="size-4" /> Key Headlines
          </h3>
          <button
            onClick={onRefresh}
            className="inline-flex items-center gap-1.5 rounded-lg border border-zinc-200 px-3 py-1.5 text-sm font-medium text-zinc-600 transition hover:bg-zinc-50"
          >
            <RefreshCw className="size-3.5" /> Refresh
          </button>
        </div>

        {brief.headlines.length === 0 ? (
          <p className="text-sm text-zinc-500">
            No distinct headlines were found. Try a more specific topic.
          </p>
        ) : (
          <ul className="divide-y divide-zinc-100">
            {brief.headlines.map((item, i) => (
              <li key={item.url || i} className="group py-4 first:pt-0 last:pb-0">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <a
                      href={item.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="font-medium leading-snug text-zinc-900 transition-colors group-hover:text-emerald-600"
                    >
                      {item.title}
                    </a>
                    {item.summary && (
                      <p className="mt-1 text-sm leading-relaxed text-zinc-500">
                        {item.summary}
                      </p>
                    )}
                    <div className="mt-2 flex items-center gap-2">
                      <span className="rounded-full bg-zinc-100 px-2 py-0.5 text-xs font-medium text-zinc-600">
                        {item.source}
                      </span>
                    </div>
                  </div>
                  <a
                    href={item.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    aria-label="Open article"
                    className="mt-0.5 shrink-0 text-zinc-300 transition-colors group-hover:text-emerald-600"
                  >
                    <ExternalLink className="size-4" />
                  </a>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

function BriefSkeleton() {
  return (
    <div className="grid gap-6 lg:grid-cols-5">
      <div className="space-y-3 rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm lg:col-span-2">
        <div className="h-4 w-32 animate-pulse rounded bg-zinc-100" />
        <div className="h-3 w-full animate-pulse rounded bg-zinc-100" />
        <div className="h-3 w-5/6 animate-pulse rounded bg-zinc-100" />
        <div className="h-3 w-2/3 animate-pulse rounded bg-zinc-100" />
      </div>
      <div className="space-y-4 rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm lg:col-span-3">
        {[0, 1, 2].map((i) => (
          <div key={i} className="space-y-2">
            <div className="h-3 w-4/5 animate-pulse rounded bg-zinc-100" />
            <div className="h-3 w-1/2 animate-pulse rounded bg-zinc-100" />
          </div>
        ))}
      </div>
    </div>
  );
}