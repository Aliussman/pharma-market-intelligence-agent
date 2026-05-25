"""LLM prompts for pharmaceutical analysis"""

PHARMA_PROMPT_TEMPLATE = """You are an expert pharmaceutical market analyst. Analyze the following financial or earnings text and provide structured insights.

Text to analyze:
{text}

Please provide a detailed analysis covering:
1. Financial Summary: Key financial metrics and performance indicators
2. Priority Brands: Leading products and their market position
3. Pipeline & Regulatory: New drugs in pipeline and regulatory status
4. Strategic Insights: Overall strategic direction and market positioning

Format your response as clear sections with headers."""

FINANCE_PROMPT_TEMPLATE = """You are an expert pharmaceutical finance analyst. Analyze the following financial results and earnings report.

Financial Text:
{text}

Focus on:
1. Revenue and Sales Growth: Year-over-year and quarterly trends
2. Profitability Metrics: Operating margins, EPS, and net income
3. Cash Flow Analysis: Free cash flow and capital allocation
4. Guidance and Outlook: Management's forward guidance and expectations

Provide quantitative analysis with specific numbers where available."""


def pharma_prompt(text: str) -> str:
    """Generate a general pharmaceutical analysis prompt"""
    return PHARMA_PROMPT_TEMPLATE.format(text=text)


def finance_prompt(text: str) -> str:
    """Generate a finance-focused analysis prompt"""
    return FINANCE_PROMPT_TEMPLATE.format(text=text)


def select_prompt(text: str) -> str:
    """Select appropriate prompt based on content"""
    from src.core.constants import FINANCE_KEYWORDS
    
    if any(word.lower() in text.lower() for word in FINANCE_KEYWORDS):
        return finance_prompt(text)
    else:
        return pharma_prompt(text)
