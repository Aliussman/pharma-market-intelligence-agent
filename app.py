from fastapi import FastAPI
from schemas import PharmaInput, PharmaOutput
from llm import run_llm
from prompts import pharma_prompt

app = FastAPI(title="Pharma Market Intelligence API")

@app.get("/")
def root():
    return {"status": "Pharma Market Intelligence API is running"}
   
@app.post("/analyze", response_model=PharmaOutput)
def analyze(data: PharmaInput):
    prompt = pharma_prompt(data.raw_text)
    analysis = run_llm(prompt)

    return {
        "company": data.company,
        "analysis": {
            "financial_summary": analysis,
            "priority_brands": analysis,
            "pipeline_regulatory": analysis,
            "strategic_insights": analysis
        }
    }
