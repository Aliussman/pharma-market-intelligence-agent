import { Activity, BrainCircuit, Globe2, Sparkles } from "lucide-react";

import { AnalyzerPanel } from "@/components/AnalyzerPanel";
import { MarketBriefPanel } from "@/components/MarketBriefPanel";

const highlights = [
  {
    icon: Globe2,
    label: "Web crawling agent",
    text: "Scans pharma news and regulatory developments automatically.",
  },
  {
    icon: BrainCircuit,
    label: "Structured AI analysis",
    text: "Turns earnings text into four executive-ready sections via LLM.",
  },
  {
    icon: Activity,
    label: "Pipeline & finance focus",
    text: "Covers financials, priority brands, pipeline, and strategy.",
  },
];

export default function Home() {
  return (
    <>
      <main className="flex-1">
        {/* Hero */}
        <section className="relative overflow-hidden border-b border-zinc-200/80 bg-gradient-to-b from-emerald-50/70 via-white to-white">
          <div
            aria-hidden
            className="pointer-events-none absolute -top-24 right-0 size-96 rounded-full bg-emerald-200/40 blur-3xl"
          />
          <div className="relative mx-auto grid w-full max-w-6xl gap-10 px-4 py-16 sm:px-6 lg:grid-cols-2 lg:py-24">
            <div>
              <span className="inline-flex items-center gap-1.5 rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700">
                <Sparkles className="size-3.5" /> AI-Powered Market Intelligence
              </span>
              <h1 className="mt-5 text-4xl font-bold leading-tight tracking-tight text-zinc-900 sm:text-5xl">
                The pharma market,{" "}
                <span className="text-emerald-600">intelligently briefed.</span>
              </h1>
              <p className="mt-4 max-w-xl text-lg leading-relaxed text-zinc-600">
                A research agent that scans the web for pharmaceutical news and
                analyzes earnings releases — delivering an executive-ready market
                brief and structured company analysis in seconds.
              </p>
              <div className="mt-8 flex flex-wrap gap-3">
                <a
                  href="#analyzer"
                  className="inline-flex h-11 items-center rounded-lg bg-emerald-600 px-6 text-sm font-semibold text-white shadow-sm transition hover:bg-emerald-500"
                >
                  Analyze Earnings
                </a>
                <a
                  href="#market-brief"
                  className="inline-flex h-11 items-center rounded-lg border border-zinc-300 bg-white px-6 text-sm font-semibold text-zinc-700 shadow-sm transition hover:bg-zinc-50"
                >
                  View Market Brief
                </a>
              </div>
            </div>

            <div className="grid gap-4 sm:grid-cols-1">
              {highlights.map((h) => (
                <div
                  key={h.label}
                  className="flex items-start gap-4 rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm"
                >
                  <span className="flex size-10 shrink-0 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600">
                    <h.icon className="size-5" />
                  </span>
                  <div>
                    <h3 className="font-semibold text-zinc-900">{h.label}</h3>
                    <p className="mt-0.5 text-sm leading-relaxed text-zinc-500">{h.text}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        <MarketBriefPanel />
        <AnalyzerPanel />
      </main>
    </>
  );
}