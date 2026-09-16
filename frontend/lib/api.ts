import type { MarketBrief, PharmaOutput } from "@/lib/types";

export const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export class ApiError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

async function handle<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let detail = `Request failed with status ${response.status}`;
    try {
      const body = await response.json();
      if (typeof body?.detail === "string") detail = body.detail;
    } catch {
      // ignore non-JSON error bodies
    }
    throw new ApiError(response.status, detail);
  }
  return response.json() as Promise<T>;
}

export function analyzeText(company: string, rawText: string): Promise<PharmaOutput> {
  return fetch(`${API_URL}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ company, raw_text: rawText }),
  }).then((r) => handle<PharmaOutput>(r));
}

export function getMarketBrief(topic: string): Promise<MarketBrief> {
  const params = new URLSearchParams({ topic });
  return fetch(`${API_URL}/market-brief?${params.toString()}`).then((r) =>
    handle<MarketBrief>(r),
  );
}

export async function downloadAnalysisPdf(result: PharmaOutput): Promise<void> {
  const response = await fetch(`${API_URL}/export/pdf`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(result),
  });
  if (!response.ok) {
    throw new ApiError(response.status, `Download failed with status ${response.status}`);
  }
  const blob = await response.blob();
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `${result.company}_pharma_intelligence.pdf`;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}