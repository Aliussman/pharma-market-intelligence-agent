# Pharma Market Intelligence AI Agent

An AI-powered market intelligence system that analyzes pharmaceutical earnings releases, investor updates, and pipeline announcements using LLM-based structured analysis to extract financial insights, key brands, regulatory milestones, and strategic recommendations.

## Tech Stack
- **FastAPI** (Backend REST API)
- **Streamlit** (Interactive Frontend Dashboard)
- **Groq LLM** (AI Analysis Engine)
- **FPDF** (PDF Export)
- **Pydantic** (Data Validation)

## Features
- Financial summary extraction (sales, margins, EPS, cash flow)
- Priority brands and growth drivers analysis
- Pipeline & regulatory insights
- Strategic analysis and recommendations
- Executive-ready PDF export

## Architecture
Streamlit UI → FastAPI → Prompt Engine → Groq LLM → Structured JSON Output

## Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**
   Create a `.env` file with your Groq API key:
   ```bash
   GROQ_API_KEY=your_api_key_here
   ```

3. **Run the application**

   Backend (FastAPI):
   ```bash
   uvicorn app:app --reload
   ```

   Frontend (Streamlit) - in a new terminal:
   ```bash
   streamlit run streamlit_app.py
   ```

   Access the Streamlit UI at `http://localhost:8501` and API docs at `http://localhost:8000/docs`
