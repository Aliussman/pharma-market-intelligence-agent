# Pharma Market Intelligence AI Agent

An AI-powered market intelligence system that analyzes pharmaceutical earnings releases and researches the pharma market using LLM-based structured analysis.

## 📋 Features

- **Financial Analysis**: Extract key financial metrics and performance indicators
- **Pipeline Intelligence**: Track drug pipeline status and regulatory updates
- **Strategic Insights**: Get market positioning and strategic recommendations
- **Autonomous Market Brief**: A research agent crawls the web (Tavily search with RSS fallback) and summarizes the latest pharma news into an executive brief
- **PDF Export**: Generate professional reports in PDF format
- **User-Friendly Dashboard**: Next.js web interface
- **RESTful API**: FastAPI backend for programmatic access

## 🏗️ Architecture

```
Next.js UI (frontend/)
         ↓  HTTP (CORS)
FastAPI Backend (src/api)
         ↓
Analysis Service (src/services/analyzer.py)
         ↓
LLM Client (src/llm)  [Groq JSON-mode structured output]
         ↓
Groq API (llama-3.1-8b-instant)

Market Brief Agent (src/services/market_brief.py)
   ├── Tavily Search API (when TAVILY_API_KEY is set)
   └── Pharma RSS feeds (fallback: Fierce Pharma, Fierce Biotech, Endpoints News)
```

## 📁 Project Structure

```
pharma-market-intelligence-agent/
├── src/
│   ├── api/              # FastAPI application (src/api/main.py)
│   ├── core/             # Configuration & constants
│   ├── llm/              # Groq LLM client & prompts
│   ├── schemas/          # Pydantic data models
│   ├── services/         # Business logic (analyzer, market brief, PDF export)
│   └── ui/               # Streamlit frontend (src/ui/app.py, superseded by Next.js)
├── frontend/             # Next.js web interface
├── tests/                # Unit tests (pytest)
├── docs/                 # Documentation
├── run.py                # API entry point
├── requirements.txt      # Production dependencies
├── requirements-dev.txt  # Development dependencies
├── pyproject.toml        # Project metadata & tooling config
└── .env.example          # Environment template
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- A [Groq](https://groq.com) API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Aliussman/pharma-market-intelligence-agent.git
   cd pharma-market-intelligence-agent
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your Groq API key
   export GROQ_API_KEY="your-api-key-here"
   # Optional: Tavily API key for web search in the market brief agent
   export TAVILY_API_KEY="your-tavily-key-here"
   ```

### Running the Application

**Start the Backend (FastAPI)**
```bash
python run.py
# API will be available at http://127.0.0.1:8000
# API Docs: http://127.0.0.1:8000/docs
```

**Start the Frontend (Next.js)**
```bash
cd frontend
cp .env.local.example .env.local   # API_URL defaults to http://127.0.0.1:8000
npm install
npm run dev                        # or: npm run build && npm start
# UI will open at http://localhost:3000
```

## 📚 API Documentation

### Health Check
```bash
GET /
```

### Analyze Pharmaceutical Data
```bash
POST /analyze

Request Body:
{
  "company": "Pfizer",
  "raw_text": "Q3 2024 earnings report showing..."
}

Response:
{
  "company": "Pfizer",
  "analysis": {
    "financial_summary": "...",
    "priority_brands": "...",
    "pipeline_regulatory": "...",
    "strategic_insights": "..."
  }
}
```

The analysis is produced with the LLM returning structured JSON across the four sections above.

### Generate a Market Brief
```bash
GET /market-brief?topic=obesity%20drugs

Response:
{
  "generated_at": "2026-01-01T00:00:00Z",
  "topic": "obesity drugs",
  "market_overview": "...",
  "headlines": [{ "title": "...", "source": "...", "url": "...", "summary": "..." }]
}
```

### Export Analysis as PDF
```bash
POST /export/pdf

Request Body:
{
  "company": "Pfizer",
  "analysis": { "financial_summary": "...", "priority_brands": "...", "pipeline_regulatory": "...", "strategic_insights": "..." }
}

# Returns an application/pdf attachment
```

The market brief agent uses the Tavily Search API when `TAVILY_API_KEY` is set; otherwise it falls back to curated pharmaceutical RSS feeds (Fierce Pharma, Fierce Biotech, Endpoints News).

**Access Interactive API Documentation:**
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 🧪 Testing

Run unit tests with pytest:

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_api.py
```

## 🔧 Tech Stack

- **Backend**: FastAPI, Uvicorn
- **Frontend**: Next.js (App Router, Tailwind CSS)
- **AI/ML**: Groq (`llama-3.1-8b-instant`), structured JSON output
- **Web Research**: Tavily Search API (optional) + RSS feeds via Feedparser
- **Data Validation**: Pydantic
- **PDF Generation**: FPDF2
- **Testing**: Pytest (backend), ESLint + build checks (frontend)
- **Code Quality**: Black, Ruff, MyPy

## 📋 Configuration

Edit `.env` to customize:

```env
GROQ_API_KEY=your_key_here
TAVILY_API_KEY=your_tavily_key_here   # optional, enables web search
LLM_MODEL=llama-3.1-8b-instant
LLM_TEMPERATURE=0.2
LLM_MAX_TOKENS=1500
API_HOST=127.0.0.1
API_PORT=8000
CORS_ORIGINS=http://localhost:3000    # frontend origin(s)
ENVIRONMENT=development
LOG_LEVEL=INFO
```

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/amazing-feature`
2. Commit changes: `git commit -m 'Add amazing feature'`
3. Push to branch: `git push origin feature/amazing-feature`
4. Open a Pull Request

## 📝 Development

### Code Style
- Follow PEP 8 guidelines
- Format code with Black: `black src/ tests/`
- Lint with Ruff: `ruff check src/ tests/`
- Type check with MyPy: `mypy src/`

### Before Committing
```bash
black src/ tests/
ruff check src/ tests/
mypy src/
pytest
```

## 📄 License

MIT License - see LICENSE file for details

## 👤 Author

Ali Usman Muhammad - [@Aliussman](https://github.com/Aliussman)

## 🙋 Support

For issues and questions, please open a GitHub issue.

---

**Note**: This project requires a Groq API key. Get one at [groq.com](https://console.groq.com).