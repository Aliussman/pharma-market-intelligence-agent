"""Configuration and settings for the application"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", 8000))
API_TITLE = "Pharma Market Intelligence API"
API_VERSION = "0.1.0"

# LLM Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = ENVIRONMENT == "development"
