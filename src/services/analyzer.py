"""Business logic for analyzing pharmaceutical text."""

import logging
from typing import Any, Optional

from src.llm.client import LLMClient
from src.llm.prompts import select_prompt
from src.schemas.models import AnalysisOutput

logger = logging.getLogger(__name__)


class AnalysisService:
    """Orchestrates text analysis through the LLM."""

    def __init__(self, llm_client: Optional[LLMClient] = None) -> None:
        self.llm = llm_client or LLMClient()

    def analyze(self, company: str, raw_text: str) -> AnalysisOutput:
        """Analyze raw financial/earnings text into a structured report."""
        prompt = select_prompt(raw_text)
        data = self.llm.run_json(prompt)

        return AnalysisOutput(
            financial_summary=self._as_text(data.get("financial_summary")),
            priority_brands=self._as_text(data.get("priority_brands")),
            pipeline_regulatory=self._as_text(data.get("pipeline_regulatory")),
            strategic_insights=self._as_text(data.get("strategic_insights")),
        )

    @staticmethod
    def _as_text(value: Any) -> str:
        if isinstance(value, str):
            return value
        if value is None:
            return "Not mentioned"
        return str(value)
