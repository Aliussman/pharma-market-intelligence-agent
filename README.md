# Pharma Market Intelligence AI Agent

An AI-powered market intelligence system that analyzes pharmaceutical earnings releases and pipeline updates using LLM-based structured analysis.

## Tech Stack
- FastAPI (Backend)
- Streamlit (Frontend)
- LLM Integration
- PDF Export

## Features
- Financial summary extraction
- Pipeline & regulatory insights
- Strategic analysis
- Executive PDF export

## Architecture
Streamlit UI → FastAPI → Prompt Engine → LLM → Structured Output

## How to Run

Backend:
uvicorn app:app --reload

Frontend:
streamlit run streamlit_app.py
