from fastapi import FastAPI
from schemas import PharmaInput, PharmaOutput
from llm import run_llm
from prompts import pharma_prompt, finance_prompt

app = FastAPI(title="Pharma Market Intelligence API")


@app.get("/")
def root():
    return {"status": "Pharma Market Intelligence API is running"}


def choose_prompt(text: str) -> str:
    finance_keywords = [
        "sales", "revenue", "net sales", "net income",
        "operating income", "EPS", "cash flow", "margin"
    ]

    if any(word.lower() in text.lower() for word in finance_keywords):
        return finance_prompt(text)
    else:
        return pharma_prompt(text)


@app.post("/analyze", response_model=PharmaOutput)
def analyze(data: PharmaInput):
    prompt = choose_prompt(data.raw_text)
    analysis = run_llm(prompt)

    return {
        "company": data.company,
        "analysis": analysis
    }

