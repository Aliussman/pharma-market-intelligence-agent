# Pharma Market Intelligence AI Agent

An AI-powered market intelligence system that analyzes pharmaceutical earnings releases and pipeline updates using LLM-based structured analysis.

## 📋 Features

- **Financial Analysis**: Extract key financial metrics and performance indicators
- **Pipeline Intelligence**: Track drug pipeline status and regulatory updates
- **Strategic Insights**: Get market positioning and strategic recommendations
- **PDF Export**: Generate professional reports in PDF format
- **User-Friendly Dashboard**: Streamlit-based web interface
- **RESTful API**: FastAPI backend for programmatic access

## 🏗️ Architecture

```
Streamlit UI (Frontend)
         ↓
FastAPI Backend (src/api)
         ↓
Analysis Service (src/services)
         ↓
LLM Client (src/llm)
         ↓
OpenAI/LLM API
```

## 📁 Project Structure

```
pharma-market-intelligence-agent/
├── src/
│   ├── api/              # FastAPI application & routes
│   ├── core/             # Configuration & constants
│   ├── llm/              # LLM client & prompts
│   ├── schemas/          # Pydantic data models
│   ├── services/         # Business logic
│   └── ui/               # Streamlit frontend
├── tests/                # Unit tests
├── docs/                 # Documentation
├── requirements.txt      # Production dependencies
├── requirements-dev.txt  # Development dependencies
├── pyproject.toml        # Project metadata
├── .env.example          # Environment template
└── run.py               # Entry point
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- OpenAI API key

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
   # Edit .env and add your OpenAI API key
   export OPENAI_API_KEY="your-api-key-here"
   ```

### Running the Application

**Start the Backend (FastAPI)**
```bash
python run.py
# API will be available at http://127.0.0.1:8000
# API Docs: http://127.0.0.1:8000/docs
```

**Start the Frontend (Streamlit)**
```bash
streamlit run src/ui/app.py
# UI will open at http://localhost:8501
```

## 📚 API Documentation

### Health Check
```bash
GET /api/
```

### Analyze Pharmaceutical Data
```bash
POST /api/analyze

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
- **Frontend**: Streamlit
- **AI/ML**: LangChain, OpenAI
- **Data Validation**: Pydantic
- **PDF Generation**: FPDF2
- **Testing**: Pytest
- **Code Quality**: Black, Ruff, MyPy

## 📋 Configuration

Edit `.env` to customize:

```env
API_HOST=127.0.0.1
API_PORT=8000
OPENAI_API_KEY=your_key_here
LLM_MODEL=gpt-4
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
- Format code with Black: `black src/`
- Lint with Ruff: `ruff check src/`
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

**Note**: This project requires an OpenAI API key. Get one at [openai.com](https://openai.com)
