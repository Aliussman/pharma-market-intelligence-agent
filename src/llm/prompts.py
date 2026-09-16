"""LLM prompts for pharmaceutical analysis."""

from src.core.constants import FINANCE_KEYWORDS

_OUTPUT_FORMAT = """Return ONLY valid JSON with exactly these four keys:
{
  "financial_summary": "Financial performance (sales, margins, EPS, cash flow).",
  "priority_brands": "Priority brands and growth drivers.",
  "pipeline_regulatory": "Pipeline and regulatory milestones.",
  "strategic_insights": "Strategic outlook and market positioning."
}

Use "Not mentioned" for any field absent from the source text."""

PHARMA_PROMPT_TEMPLATE = """You are a senior pharma market intelligence analyst.

Analyze the following announcement. Focus on products, pipeline developments, and regulatory
status.

TEXT:
{text}

RULES:
- Use only information explicitly stated in the text. Do NOT hallucinate.
- If a field is missing, write "Not mentioned".

{output_format}"""

FINANCE_PROMPT_TEMPLATE = """You are a senior pharma financial and strategy analyst.

Analyze the following earnings or business update.

TEXT:
{text}

RULES:
- Use only information explicitly stated in the text. Do NOT hallucinate.
- If a field is missing, write "Not mentioned".
- Be concise, structured, and executive-ready.

{output_format}"""


def pharma_prompt(text: str) -> str:
    """Generate a pharmaceutical / pipeline analysis prompt."""
    return PHARMA_PROMPT_TEMPLATE.format(text=text, output_format=_OUTPUT_FORMAT)


def finance_prompt(text: str) -> str:
    """Generate a finance-focused analysis prompt."""
    return FINANCE_PROMPT_TEMPLATE.format(text=text, output_format=_OUTPUT_FORMAT)


def select_prompt(text: str) -> str:
    """Choose the appropriate prompt based on the text content."""
    lowered = text.lower()
    if any(keyword.lower() in lowered for keyword in FINANCE_KEYWORDS):
        return finance_prompt(text)
    return pharma_prompt(text)


_MARKET_BRIEF_OUTPUT_FORMAT = """Return ONLY valid JSON with exactly these keys:
{
  "market_overview": "A concise executive summary (3-5 sentences) of the overall state of
                      the pharma market based ONLY on the articles.",
  "headlines": [
    {
      "title": "Original headline title",
      "source": "Source name",
      "url": "Original article URL",
      "summary": "One-sentence explanation of why it matters"
    }
  ]
}

Rules:
- Select the 5-8 most relevant and distinct news stories.
- Do NOT invent facts, quotes, or URLs not present in the source material.
- If the market overview has no information, write 'Insufficient data from the recent articles'."""

MARKET_BRIEF_PROMPT_TEMPLATE = """You are a senior pharma market intelligence analyst compiling a
concise executive briefing.

Topic: {topic}

Below are recently collected pharma news items (title, source, snippet):

{articles}

{mkt_output_format}"""


def market_brief_prompt(topic: str, articles: str) -> str:
    """Generate a prompt that condenses collected news items into a market brief."""
    return MARKET_BRIEF_PROMPT_TEMPLATE.format(
        topic=topic,
        articles=articles,
        mkt_output_format=_MARKET_BRIEF_OUTPUT_FORMAT,
    )


def format_articles_for_prompt(items: list[dict]) -> str:
    """Format gathered news items into a numbered digest for the LLM."""
    lines = []
    for i, item in enumerate(items, start=1):
        title = item.get("title", "Untitled")
        source = item.get("source", "Unknown")
        snippet = item.get("snippet", item.get("summary", ""))[:500]
        url = item.get("url", "")
        lines.append(f"{i}. [{source}] {title}\n   {snippet}\n   URL: {url}")
    return "\n\n".join(lines) or "No articles were collected."
