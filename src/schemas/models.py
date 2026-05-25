"""Data models and schemas for the API"""
from pydantic import BaseModel, Field
from typing import Optional, Dict


class PharmaInput(BaseModel):
    """Input schema for pharmaceutical analysis"""
    company: str = Field(..., description="Company name")
    raw_text: str = Field(..., description="Raw financial or earnings text to analyze")

    class Config:
        schema_extra = {
            "example": {
                "company": "Pharma Corp",
                "raw_text": "Q3 2024 earnings report showing 8% revenue growth..."
            }
        }


class AnalysisOutput(BaseModel):
    """Output schema for analysis results"""
    financial_summary: str = Field(..., description="Financial summary analysis")
    priority_brands: str = Field(..., description="Priority brands analysis")
    pipeline_regulatory: str = Field(..., description="Pipeline and regulatory insights")
    strategic_insights: str = Field(..., description="Strategic insights")


class PharmaOutput(BaseModel):
    """Complete API response schema"""
    company: str = Field(..., description="Company name")
    analysis: AnalysisOutput = Field(..., description="Analysis results")

    class Config:
        schema_extra = {
            "example": {
                "company": "Pharma Corp",
                "analysis": {
                    "financial_summary": "Analysis here...",
                    "priority_brands": "Analysis here...",
                    "pipeline_regulatory": "Analysis here...",
                    "strategic_insights": "Analysis here..."
                }
            }
        }
