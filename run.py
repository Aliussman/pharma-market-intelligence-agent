"""Application entry point."""

import uvicorn

from src.api.main import app
from src.core.config import API_HOST, API_PORT, DEBUG

if __name__ == "__main__":
    uvicorn.run(app, host=API_HOST, port=API_PORT, reload=DEBUG)
