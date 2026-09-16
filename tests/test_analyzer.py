"""Tests for the analysis service."""

from src.schemas.models import AnalysisOutput
from src.services.analyzer import AnalysisService


class FakeLLM:
    """Stub LLM client returning canned JSON."""

    def __init__(self, payload):
        self.payload = payload
        self.last_prompt = None

    def run_json(self, prompt):
        self.last_prompt = prompt
        return self.payload


def test_analyze_maps_all_sections():
    payload = {
        "financial_summary": "Revenue up 8%",
        "priority_brands": "Brand A led growth",
        "pipeline_regulatory": "Phase 3 trial ongoing",
        "strategic_insights": "Poised for expansion",
    }
    service = AnalysisService(llm_client=FakeLLM(payload))
    result = service.analyze(company="Pharma Co", raw_text="Sales grew 8%")

    assert isinstance(result, AnalysisOutput)
    assert result.financial_summary == "Revenue up 8%"
    assert result.priority_brands == "Brand A led growth"
    assert result.pipeline_regulatory == "Phase 3 trial ongoing"
    assert result.strategic_insights == "Poised for expansion"


def test_analyze_defaults_missing_sections():
    service = AnalysisService(llm_client=FakeLLM({}))
    result = service.analyze(company="Pharma Co", raw_text="Some text")

    assert result.financial_summary == "Not mentioned"
    assert result.priority_brands == "Not mentioned"
    assert result.pipeline_regulatory == "Not mentioned"
    assert result.strategic_insights == "Not mentioned"


def test_analyze_coerces_non_string_values():
    service = AnalysisService(llm_client=FakeLLM({"financial_summary": 123}))
    result = service.analyze(company="Pharma Co", raw_text="Some text")
    assert result.financial_summary == "123"
