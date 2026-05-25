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
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 2000

# API Response Keys
ANALYSIS_SECTIONS = [
    "financial_summary",
    "priority_brands",
    "pipeline_regulatory",
    "strategic_insights",
]
