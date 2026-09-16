"""Tests for the PDF export service."""

from src.services.pdf_export import PDFExportService


def test_create_pdf_returns_pdf_bytes():
    content = "Revenue grew 8% last quarter."
    pdf = PDFExportService.create_pdf(content, title="Test Report")
    assert isinstance(pdf, bytes)
    assert pdf.startswith(b"%PDF")


def test_format_analysis_for_export_includes_sections():
    analysis = {
        "financial_summary": "Revenue up",
        "priority_brands": "Brand A",
        "pipeline_regulatory": "Phase 3",
        "strategic_insights": "Expand",
    }
    text = PDFExportService.format_analysis_for_export("Pharma Co", analysis)
    headers = [
        "FINANCIAL SUMMARY",
        "PRIORITY BRANDS",
        "PIPELINE & REGULATORY",
        "STRATEGIC INSIGHTS",
    ]
    for header in headers:
        assert header in text
    assert "Pharma Co" in text
