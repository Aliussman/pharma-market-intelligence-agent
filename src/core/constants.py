"""Constants used throughout the application"""

# Financial Keywords for prompt selection
FINANCE_KEYWORDS = [
    "sales",
    "revenue",
    "net sales",
    "net income",
    "operating income",
    "EPS",
    "cash flow",
    "margin",
    "earnings",
    "profit",
    "quarterly",
    "annual",
]

# LLM Defaults
DEFAULT_TEMPERATURE = 0.2
DEFAULT_MAX_TOKENS = 1500

# API Response Keys
ANALYSIS_SECTIONS = [
    "financial_summary",
    "priority_brands",
    "pipeline_regulatory",
    "strategic_insights",
]

# Market Brief Queries (used with Tavily when configured)
MARKET_BRIEF_QUERIES = [
    "pharmaceutical industry market news today",
    "big pharma pipeline regulatory updates",
    "pharma earnings and financial results",
]

# Curated pharma news feeds (RSS fallback when no Tavily key)
PHARMA_RSS_FEEDS = [
    ("Fierce Pharma", "https://www.fiercepharma.com/rss/xml"),
    ("Fierce Biotech", "https://www.fiercebiotech.com/rss/xml"),
    ("Endpoints News", "https://endpts.com/feed/"),
]

# Tavily API
TAVILY_SEARCH_URL = "https://api.tavily.com/search"
TAVILY_EXTRACT_URL = "https://api.tavily.com/extract"
