# -------- Pharma / Clinical Prompt --------
def pharma_prompt(text: str) -> str:
    return f"""
You are a senior pharma market intelligence analyst.

Analyze the following pharma-related announcement.

RULES:
- Do NOT assume information not explicitly stated.
- If a field is missing, say "Not mentioned".
- If multiple products are mentioned, analyze each separately.
- Do NOT hallucinate.

Extract:
- Product name
- Product type (drug, vaccine, gene therapy, etc.)
- Indication / disease area
- Clinical or regulatory status
- Key milestones

TEXT:
{text}

OUTPUT:
Use clear headings and bullet points.
"""


# -------- Financial / Earnings Prompt --------
def finance_prompt(text: str) -> str:
    return f"""
You are a senior pharma financial and strategy analyst.

Analyze the following earnings or business update.

TASKS:
1. Summarize financial performance (sales, margins, EPS, cash flow).
2. Identify priority brands and growth drivers.
3. Extract pipeline and regulatory milestones.
4. Provide strategic insights based only on the text.

RULES:
- Do NOT hallucinate.
- If information is missing, say "Not mentioned".
- Be concise, structured, and executive-ready.

TEXT:
{text}

OUTPUT STRUCTURE:
- Financial Performance Summary
- Priority Brand Performance
- Pipeline & Regulatory Milestones
- Strategic Insights
"""
