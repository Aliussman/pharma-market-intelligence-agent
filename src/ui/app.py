"""Streamlit frontend for the Pharma Market Intelligence Agent."""

import requests
import streamlit as st

from src.services.pdf_export import PDFExportService

API_URL = "http://127.0.0.1:8000/analyze"

st.set_page_config(
    page_title="Pharma Market Intelligence",
    page_icon="💊",
    layout="wide",
)

st.title("💊 Pharma Market Intelligence Dashboard")
st.caption("AI-powered analysis of pharmaceutical financial performance & pipeline updates")
st.divider()

# ---------------- INPUT ----------------
st.subheader("📄 Input Financial / Earnings Text")

company = st.text_input("Company", value="Pharma Company")

raw_text = st.text_area(
    "Paste company earnings release, investor update, or press statement",
    height=220,
    placeholder="Paste full-year or quarterly pharma financial results here...",
)

analyze_btn = st.button("🔍 Analyze", use_container_width=True)

# ---------------- API CALL ----------------
if analyze_btn:
    if not raw_text.strip():
        st.warning("Please paste some text to analyze.")
    else:
        with st.spinner("Analyzing with AI…"):
            try:
                response = requests.post(
                    API_URL,
                    json={"company": company, "raw_text": raw_text},
                    timeout=120,
                )
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the backend API. Is it running?")
                st.stop()

        if response.status_code == 200:
            result = response.json()

            st.success("Analysis completed successfully")

            # ---------------- TABS ----------------
            tab1, tab2, tab3, tab4 = st.tabs(
                [
                    "📈 Financial Summary",
                    "💊 Priority Brands",
                    "🧬 Pipeline & Regulatory",
                    "🧠 Strategic Insights",
                ]
            )

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

            export_text = PDFExportService.format_analysis_for_export(
                company=result["company"], analysis=result["analysis"]
            )
            pdf_bytes = PDFExportService.create_pdf(
                export_text, title="Pharma Market Intelligence Report"
            )

            st.download_button(
                label="⬇️ Download as PDF",
                data=pdf_bytes,
                file_name=f"{result['company']}_pharma_intelligence.pdf",
                mime="application/pdf",
            )
        else:
            detail = response.json().get("detail", "Unknown error")
            st.error(f"Analysis failed: {detail}")
