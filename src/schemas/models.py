"""Data models and schemas for the API"""

from pydantic import BaseModel, ConfigDict, Field


class PharmaInput(BaseModel):
    """Input schema for pharmaceutical analysis"""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "company": "Pharma Corp",
                "raw_text": "Q3 2024 earnings report showing 8% revenue growth...",
            }
        }
    )

    company: str = Field(..., description="Company name")
    raw_text: str = Field(..., description="Raw financial or earnings text to analyze")


class AnalysisOutput(BaseModel):
    """Output schema for analysis results"""

    financial_summary: str = Field(..., description="Financial summary analysis")
    priority_brands: str = Field(..., description="Priority brands analysis")
    pipeline_regulatory: str = Field(..., description="Pipeline and regulatory insights")
    strategic_insights: str = Field(..., description="Strategic insights")


class PharmaOutput(BaseModel):
    """Complete API response schema"""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "company": "Pharma Corp",
                "analysis": {
                    "financial_summary": "Analysis here...",
                    "priority_brands": "Analysis here...",
                    "pipeline_regulatory": "Analysis here...",
                    "strategic_insights": "Analysis here...",
                },
            }
        }
    )

    company: str = Field(..., description="Company name")
    analysis: AnalysisOutput = Field(..., description="Analysis results")


class MarketBriefItem(BaseModel):
    """A single headline from the market brief."""

    title: str = Field(..., description="Headline title")
    source: str = Field(..., description="Publication or source name")
    url: str = Field(..., description="Link to the article")
    summary: str = Field(..., description="One-sentence relevance summary")


class MarketBriefOutput(BaseModel):
    """Structured market intelligence brief."""

    generated_at: str = Field(..., description="ISO timestamp of generation")
    topic: str = Field(..., description="Topic the brief was generated for")
    market_overview: str = Field(..., description="LLM-written overview of the market")
    headlines: list[MarketBriefItem] = Field(..., description="Key headlines found")
