import streamlit as st
import requests
from fpdf import FPDF


# ---------------- PDF FUNCTION ----------------
def create_pdf(text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=11)

    for line in text.split("\n"):
        pdf.multi_cell(0, 8, line)

    return pdf.output(dest="S").encode("latin-1")


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Pharma Market Intelligence",
    page_icon="💊",
    layout="wide"
)

# ---------------- HEADER ----------------
st.title("💊 Pharma Market Intelligence Dashboard")
st.caption("AI-powered analysis of pharmaceutical financial performance & pipeline updates")
st.divider()

# ---------------- INPUT ----------------
st.subheader("📄 Input Financial / Earnings Text")

raw_text = st.text_area(
    "Paste company earnings release, investor update, or press statement",
    height=220,
    placeholder="Paste full-year or quarterly pharma financial results here..."
)

analyze_btn = st.button("🔍 Analyze", use_container_width=True)

# ---------------- API CALL ----------------
if analyze_btn:

    if not raw_text.strip():
        st.warning("Please paste some text to analyze.")

    else:
        with st.spinner("Analyzing with AI…"):
            response = requests.post(
                "http://127.0.0.1:8000/analyze",
                json={
                    "company": "Pharma Company",
                    "raw_text": raw_text
                }
            )

        if response.status_code == 200:
            result = response.json()

            st.success("Analysis completed successfully")

            # ---------------- KPI METRICS ----------------
            st.subheader("📊 Key Performance Indicators")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Net Sales Growth", "+8%")
            col2.metric("Core Operating Margin", "40.1%")
            col3.metric("Core EPS", "USD 8.98")
            col4.metric("Free Cash Flow", "USD 17.6B")

            st.divider()

            # ---------------- TABS ----------------
            tab1, tab2, tab3, tab4 = st.tabs([
                "📈 Financial Summary",
                "💊 Priority Brands",
                "🧬 Pipeline & Regulatory",
                "🧠 Strategic Insights"
            ])

            with tab1:
                st.markdown(result["analysis"]["financial_summary"])

            with tab2:
                st.markdown(result["analysis"]["priority_brands"])

            with tab3:
                st.markdown(result["analysis"]["pipeline_regulatory"])

            with tab4:
                st.markdown(result["analysis"]["strategic_insights"])

            # ---------------- EXPORT ----------------
            st.divider()
            st.subheader("📥 Export Analysis")

            export_text = f"""
COMPANY: {result['company']}

========================
FINANCIAL SUMMARY
========================
{result['analysis']['financial_summary']}

========================
PRIORITY BRANDS
========================
{result['analysis']['priority_brands']}

========================
PIPELINE & REGULATORY
========================
{result['analysis']['pipeline_regulatory']}

========================
STRATEGIC INSIGHTS
========================
{result['analysis']['strategic_insights']}
"""

            pdf_bytes = create_pdf(export_text)

            st.download_button(
                label="⬇️ Download as PDF",
                data=pdf_bytes,
                file_name=f"{result['company']}_pharma_intelligence.pdf",
                mime="application/pdf"
            )

        else:
            st.error("Could not connect to backend API")
