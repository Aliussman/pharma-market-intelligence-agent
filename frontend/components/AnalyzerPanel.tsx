"use client";

import { useEffect, useState } from "react";
import { Download, LoaderCircle, ScanLine } from "lucide-react";

import { analyzeText, ApiError, downloadAnalysisPdf } from "@/lib/api";
import type { PharmaOutput } from "@/lib/types";

const TABS = [
  { key: "financial_summary", label: "Financial Summary", icon: "📈" },
  { key: "priority_brands", label: "Priority Brands", icon: "💊" },
  { key: "pipeline_regulatory", label: "Pipeline & Regulatory", icon: "🧬" },
  { key: "strategic_insights", label: "Strategic Insights", icon: "🧠" },
] as const;

type AnalysisState =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "error"; message: string }
  | { status: "ready"; result: PharmaOutput };

export function AnalyzerPanel() {
  const [company, setCompany] = useState("Pharma Company");
  const [rawText, setRawText] = useState("");
  const [state, setState] = useState<AnalysisState>({ status: "idle" });
  const [activeTab, setActiveTab] =
    useState<(typeof TABS)[number]["key"]>("financial_summary");
  const [downloading, setDownloading] = useState(false);
  const [downloadError, setDownloadError] = useState<string | null>(null);
  const isReady = state.status === "ready";

  useEffect(() => {
    if (isReady) {
      document.getElementById("analyzer")?.scrollIntoView({ behavior: "smooth" });
    }
  }, [isReady]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!rawText.trim()) return;
    setState({ status: "loading" });
    try {
      const result = await analyzeText(company.trim() || "Pharma Company", rawText);
      setState({ status: "ready", result });
    } catch (err) {
      const message =
        err instanceof ApiError ? err.message : "Could not reach the backend API.";
      setState({ status: "error", message });
    }
  }

  async function handleDownload() {
    if (state.status !== "ready" || downloading) return;
    setDownloading(true);
    setDownloadError(null);
    try {
      await downloadAnalysisPdf(state.result);
    } catch {
      setDownloadError("PDF download failed. Is the backend API running?");
    } finally {
      setDownloading(false);
    }
  }

  return (
    <section
      id="analyzer"
      className="border-t border-zinc-200/80 bg-zinc-50/70"
    >
      <div className="mx-auto w-full max-w-6xl px-4 py-14 sm:px-6">
        <div className="mb-2 flex items-center gap-2 text-sm font-semibold uppercase tracking-wider text-emerald-600">
          <ScanLine className="size-4" /> Earnings & Pipeline Analysis
        </div>
        <h2 className="text-2xl font-bold tracking-tight text-zinc-900 sm:text-3xl">
          Analyze an Earnings Release
        </h2>
        <p className="mt-1 text-zinc-500">
          Paste a company update and get a structured, LLM-generated report across four sections.
        </p>

        <form
          onSubmit={handleSubmit}
          className="mt-8 rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm sm:p-6"
        >
          <label className="mb-1.5 block text-sm font-medium text-zinc-700">
            Company
          </label>
          <input
            value={company}
            onChange={(e) => setCompany(e.target.value)}
            placeholder="Company name"
            className="mb-5 h-10 w-full rounded-lg border border-zinc-300 bg-white px-3 text-sm text-zinc-900 shadow-sm outline-none transition focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/30 sm:max-w-sm"
          />

          <label className="mb-1.5 block text-sm font-medium text-zinc-700">
            Financial / Earnings Text
          </label>
          <textarea
            value={rawText}
            onChange={(e) => setRawText(e.target.value)}
            rows={9}
            placeholder="Paste full-year or quarterly pharma financial results, press statement, or investor update here…"
            className="w-full resize-y rounded-lg border border-zinc-300 bg-white px-3 py-2.5 text-sm text-zinc-900 shadow-sm outline-none transition focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/30"
          />

          <button
            type="submit"
            disabled={state.status === "loading" || !rawText.trim()}
            className="mt-5 inline-flex h-11 items-center gap-2 rounded-lg bg-emerald-600 px-6 text-sm font-semibold text-white shadow-sm transition hover:bg-emerald-500 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {state.status === "loading" ? (
              <>
                <LoaderCircle className="size-4 animate-spin" /> Analyzing…
              </>
            ) : (
              <>Analyze</>
            )}
          </button>
        </form>

        {state.status === "error" && (
          <div className="mt-5 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {state.message}
          </div>
        )}

        {state.status === "ready" && (
          <div className="mt-6 rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm sm:p-6">
            <div className="mb-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <h3 className="text-lg font-semibold text-zinc-900">
                {state.result.company} — Analysis Results
              </h3>
              <button
                onClick={handleDownload}
                disabled={downloading}
                className="inline-flex h-9 items-center gap-1.5 rounded-lg bg-zinc-900 px-3.5 text-sm font-medium text-white shadow-sm transition hover:bg-zinc-700 disabled:opacity-60"
              >
                {downloading ? (
                  <LoaderCircle className="size-4 animate-spin" />
                ) : (
                  <Download className="size-4" />
                )}
                Download PDF
              </button>
            </div>
            {downloadError && (
              <div className="mb-3 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
                {downloadError}
              </div>
            )}

            <div className="flex flex-wrap gap-1.5 border-b border-zinc-200 pb-px">
              {TABS.map((tab) => (
                <button
                  key={tab.key}
                  onClick={() => setActiveTab(tab.key)}
                  className={`inline-flex items-center gap-1.5 rounded-t-lg border-b-2 px-3.5 py-2 text-sm font-medium transition ${
                    activeTab === tab.key
                      ? "border-emerald-600 text-emerald-700"
                      : "border-transparent text-zinc-500 hover:text-zinc-800"
                  }`}
                >
                  <span>{tab.icon}</span>
                  {tab.label}
                </button>
              ))}
            </div>

            <div className="mt-4">
              <p className="whitespace-pre-wrap leading-relaxed text-zinc-700">
                {state.result.analysis[activeTab]}
              </p>
            </div>
          </div>
        )}
      </div>
    </section>
  );
}