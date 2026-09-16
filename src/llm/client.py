"""LLM client for interacting with Groq-hosted models."""

import json
from typing import Any, Dict

from groq import APIError, Groq

from src.core.config import GROQ_API_KEY, LLM_MAX_TOKENS, LLM_MODEL, LLM_TEMPERATURE

SYSTEM_MESSAGE = (
    "You are a senior pharma market intelligence analyst. " "Always respond with valid JSON only."
)


class LLMClient:
    """Client for LLM operations against the Groq API."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str = LLM_MODEL,
        temperature: float = LLM_TEMPERATURE,
        max_tokens: int = LLM_MAX_TOKENS,
        system_message: str = SYSTEM_MESSAGE,
    ) -> None:
        self.api_key = api_key or GROQ_API_KEY
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.system_message = system_message

    def _client(self) -> Groq:
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable not set")
        return Groq(api_key=self.api_key)

    def run(self, prompt: str) -> str:
        """Send a prompt and return the raw text response."""
        response = self._complete(prompt, json_mode=False)
        content = response.choices[0].message.content
        if not content:
            raise RuntimeError("LLM returned an empty response")
        return content

    def run_json(self, prompt: str) -> Dict[str, Any]:
        """Send a prompt and parse the response as JSON (Groq JSON mode)."""
        response = self._complete(prompt, json_mode=True)
        content = response.choices[0].message.content
        if not content:
            raise RuntimeError("LLM returned an empty response")
        try:
            return json.loads(content)
        except (json.JSONDecodeError, TypeError) as exc:
            raise RuntimeError(f"LLM returned invalid JSON: {content!r}") from exc

    def _complete(self, prompt: str, *, json_mode: bool):
        """Call the Groq chat completions API, converting API failures to RuntimeError."""
        kwargs: Dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self.system_message},
                {"role": "user", "content": prompt},
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        try:
            return self._client().chat.completions.create(**kwargs)
        except APIError as exc:
            raise RuntimeError(f"Groq API error: {exc}") from exc
