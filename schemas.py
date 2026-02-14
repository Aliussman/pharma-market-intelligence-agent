from pydantic import BaseModel

class PharmaInput(BaseModel):
    company: str
    raw_text: str

class PharmaAnalysis(BaseModel):
    financial_summary: str
    priority_brands: str
    pipeline_regulatory: str
    strategic_insights: str

class PharmaOutput(BaseModel):
    company: str
    analysis: PharmaAnalysis

