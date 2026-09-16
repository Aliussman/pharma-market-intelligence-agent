export type Analysis = {
  financial_summary: string;
  priority_brands: string;
  pipeline_regulatory: string;
  strategic_insights: string;
};

export type PharmaOutput = {
  company: string;
  analysis: Analysis;
};

export type MarketBriefItem = {
  title: string;
  source: string;
  url: string;
  summary: string;
};

export type MarketBrief = {
  generated_at: string;
  topic: string;
  market_overview: string;
  headlines: MarketBriefItem[];
};