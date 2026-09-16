"""PDF export service"""

from typing import Optional

from fpdf import FPDF


class PDFExportService:
    """Service for exporting analysis results to PDF"""

    @staticmethod
    def create_pdf(content: str, title: Optional[str] = None) -> bytes:
        """
        Create a PDF from text content

        Args:
            content: Text content to include in PDF
            title: Optional title for the document

        Returns:
            PDF file as bytes
        """
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Add title if provided
        if title:
            pdf.set_font("helvetica", "B", size=16)
            pdf.multi_cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(10)

        # Add content
        pdf.set_font("helvetica", size=11)
        for line in content.split("\n"):
            if not line.strip():
                continue
            pdf.multi_cell(0, 8, line, new_x="LMARGIN", new_y="NEXT")

        result = pdf.output()
        if isinstance(result, str):
            return result.encode("latin-1", errors="replace")
        return bytes(result)

    @staticmethod
    def format_analysis_for_export(company: str, analysis: dict) -> str:
        """
        Format analysis results for PDF export

        Args:
            company: Company name
            analysis: Analysis results dictionary

        Returns:
            Formatted text string
        """
        export_text = f"""
PHARMACEUTICAL MARKET INTELLIGENCE REPORT
Company: {company}
{"="*60}

FINANCIAL SUMMARY
{"-"*60}
{analysis.get('financial_summary', 'N/A')}

PRIORITY BRANDS
{"-"*60}
{analysis.get('priority_brands', 'N/A')}

PIPELINE & REGULATORY
{"-"*60}
{analysis.get('pipeline_regulatory', 'N/A')}

STRATEGIC INSIGHTS
{"-"*60}
{analysis.get('strategic_insights', 'N/A')}
"""
        return export_text
