# Deployment Guide

## Local Development

### Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Running
```bash
# Terminal 1: Start API
python main.py

# Terminal 2: Start UI
streamlit run src/ui/app.py
```

## Heroku Deployment

### Prerequisites
- Heroku CLI installed
- Heroku account

### Steps
```bash
heroku login
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your_key_here
git push heroku refactor/project-restructure:main
```

## Docker Deployment

### Build Image
```bash
docker build -t pharma-agent .
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key pharma-agent
```

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `API_HOST`: API host (default: 127.0.0.1)
- `API_PORT`: API port (default: 8000)
- `ENVIRONMENT`: development/production (default: development)
- `LOG_LEVEL`: Logging level (default: INFO)
