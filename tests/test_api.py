"""Tests for the FastAPI application."""

from fastapi.testclient import TestClient

from src.api.main import app
from src.schemas.models import AnalysisOutput

client = TestClient(app)


def test_root_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "Pharma Market Intelligence API is running"}


def test_analyze_returns_structured_output(monkeypatch):
    def fake_analyze(company, raw_text):
        return AnalysisOutput(
            financial_summary="Revenue up 8%",
            priority_brands="Brand A",
            pipeline_regulatory="Phase 3 ongoing",
            strategic_insights="Expand globally",
        )

    monkeypatch.setattr("src.api.main.service.analyze", fake_analyze)

    response = client.post(
        "/analyze",
        json={"company": "Pharma Co", "raw_text": "Quarterly sales grew 8% with strong EPS."},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["company"] == "Pharma Co"
    assert body["analysis"]["financial_summary"] == "Revenue up 8%"
    assert body["analysis"]["priority_brands"] == "Brand A"
    assert body["analysis"]["pipeline_regulatory"] == "Phase 3 ongoing"
    assert body["analysis"]["strategic_insights"] == "Expand globally"


def test_analyze_returns_502_on_llm_failure(monkeypatch):
    def fake_analyze(company, raw_text):
        raise RuntimeError("LLM returned invalid JSON")

    monkeypatch.setattr("src.api.main.service.analyze", fake_analyze)

    response = client.post(
        "/analyze",
        json={"company": "Pharma Co", "raw_text": "Some text"},
    )

    assert response.status_code == 502
    assert "invalid JSON" in response.json()["detail"]


def test_analyze_validates_input():
    response = client.post("/analyze", json={"company": "Pharma Co"})
    assert response.status_code == 422


def test_export_pdf_returns_pdf(monkeypatch):
    payload = {
        "company": "Pharma Co",
        "analysis": {
            "financial_summary": "Revenue up 8%",
            "priority_brands": "Brand A",
            "pipeline_regulatory": "Phase 3",
            "strategic_insights": "Expand",
        },
    }
    response = client.post("/export/pdf", json=payload)
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/pdf")
    assert "attachment" in response.headers["content-disposition"]
    assert response.content.startswith(b"%PDF")
