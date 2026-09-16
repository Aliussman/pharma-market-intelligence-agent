"""Autonomous market-intelligence agent that gathers and summarizes pharma news."""

import logging
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import feedparser
import httpx

from src.core.config import BRIEF_MAX_SOURCES, TAVILY_API_KEY, TAVILY_MAX_RESULTS
from src.core.constants import (
    MARKET_BRIEF_QUERIES,
    PHARMA_RSS_FEEDS,
    TAVILY_SEARCH_URL,
)
from src.llm.client import LLMClient
from src.llm.prompts import format_articles_for_prompt, market_brief_prompt
from src.schemas.models import MarketBriefItem, MarketBriefOutput

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = httpx.Timeout(15.0)
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}


class ArticleSource(ABC):
    """A source that can gather pharma news items."""

    name: str = "base"

    @abstractmethod
    def gather(self, topic: str, limit: int) -> List[Dict[str, Any]]:
        """Return up to ``limit`` news items as dicts with title/source/url/snippet."""


class TavilySource(ArticleSource):
    """Web-search source backed by the Tavily API."""

    name = "tavily"

    def __init__(
        self,
        api_key: str,
        max_results: int = TAVILY_MAX_RESULTS,
        client: Optional[httpx.Client] = None,
    ) -> None:
        self.api_key = api_key
        self.max_results = max_results
        self._client = client

    def gather(self, topic: str, limit: int) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        seen_urls = set()
        queries = [topic] + MARKET_BRIEF_QUERIES if topic else MARKET_BRIEF_QUERIES
        for query in queries:
            if len(results) >= limit:
                break
            payload = {
                "api_key": self.api_key,
                "query": query,
                "max_results": self.max_results,
                "search_depth": "basic",
                "include_domains": [
                    "fiercepharma.com",
                    "biospace.com",
                    "reuters.com",
                    "endpoints.com",
                ],
            }
            data = self._request(TAVILY_SEARCH_URL, payload)
            for hit in data.get("results", []):
                url = hit.get("url", "")
                if url and url in seen_urls:
                    continue
                if url:
                    seen_urls.add(url)
                results.append(
                    {
                        "title": hit.get("title", ""),
                        "url": url,
                        "source": self._domain(url),
                        "snippet": hit.get("content", ""),
                    }
                )
                if len(results) >= limit:
                    break
        return results[:limit]

    def _request(self, url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if self._client is not None:
            response = self._client.post(url, json=payload)
        else:
            with httpx.Client(timeout=REQUEST_TIMEOUT) as client:
                response = client.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _domain(url: str) -> str:
        host = url.split("/")[2] if url.startswith(("http://", "https://")) else url
        return host.replace("www.", "")


class RSSSource(ArticleSource):
    """News source that polls curated RSS feeds."""

    name = "rss"

    def __init__(
        self,
        feeds: Optional[list] = None,
        per_feed: int = 4,
        client: Optional[httpx.Client] = None,
    ) -> None:
        self.feeds = feeds or PHARMA_RSS_FEEDS
        self.per_feed = per_feed
        self._client = client

    def gather(self, topic: str, limit: int) -> List[Dict[str, Any]]:
        items: List[Dict[str, Any]] = []
        per_feed = max(1, limit // max(1, len(self.feeds)))
        for label, url in self.feeds:
            items.extend(self._fetch_feed(label, url)[:per_feed])
            if len(items) >= limit:
                break
        return items[:limit]

    def _fetch_feed(self, label: str, url: str) -> List[Dict[str, Any]]:
        try:
            if self._client is not None:
                response = self._client.get(url, headers=DEFAULT_HEADERS)
            else:
                with httpx.Client(
                    timeout=REQUEST_TIMEOUT, follow_redirects=True, headers=DEFAULT_HEADERS
                ) as client:
                    response = client.get(url)
            response.raise_for_status()
            feed = feedparser.parse(response.content)
        except Exception as exc:  # noqa: BLE001 - a bad feed must not kill the whole agent
            logger.warning("Skipping feed %s: %s", label, exc)
            return []

        items = []
        for entry in feed.entries:
            title = _clean_snippet(entry.get("title", ""))
            link = entry.get("link", "")
            if not title or not link:
                continue
            items.append(
                {
                    "title": title,
                    "url": link,
                    "source": label,
                    "snippet": _clean_snippet(entry.get("summary", entry.get("description", ""))),
                }
            )
        return items


def _clean_snippet(raw: str) -> str:
    """Strip HTML tags from an RSS summary."""
    import re

    text = re.sub(r"<[^>]+>", " ", raw or "")
    return " ".join(text.split())


class MarketBriefAgent:
    """Orchestrates gathering + LLM digesting into a structured market brief."""

    def __init__(
        self,
        llm_client: Optional[LLMClient] = None,
        sources: Optional[List[ArticleSource]] = None,
    ) -> None:
        self.llm = llm_client or LLMClient()
        self.sources = sources or self._default_sources()

    @staticmethod
    def _default_sources() -> List[ArticleSource]:
        if TAVILY_API_KEY:
            return [TavilySource(api_key=TAVILY_API_KEY)]
        return [RSSSource()]

    def generate_brief(self, topic: str = "pharmaceutical industry") -> MarketBriefOutput:
        """Gather news across sources, dedupe, and condense into a brief."""
        items = self._gather_items(topic)
        if not items:
            raise RuntimeError("Could not gather any news sources; is the network reachable?")

        digest = format_articles_for_prompt(items)
        prompt = market_brief_prompt(topic=topic, articles=digest)
        try:
            data = self.llm.run_json(prompt)
        except RuntimeError:
            logger.exception("Market brief LLM digest failed")
            raise

        return self._to_model(data, topic)

    def _gather_items(self, topic: str) -> List[Dict[str, Any]]:
        gathered: List[Dict[str, Any]] = []
        seen_urls = set()
        for source in self.sources:
            try:
                for item in source.gather(topic, BRIEF_MAX_SOURCES):
                    url = item.get("url", "")
                    if url and url in seen_urls:
                        continue
                    if url:
                        seen_urls.add(url)
                    gathered.append(item)
            except Exception as exc:  # noqa: BLE001 - one failing source is non-fatal
                logger.warning("Source %s failed: %s", source.name, exc)
        return gathered[:BRIEF_MAX_SOURCES]

    @staticmethod
    def _to_model(data: Dict[str, Any], topic: str) -> MarketBriefOutput:
        overview = data.get("market_overview") or "Insufficient data from the recent articles."
        headlines = []
        for row in data.get("headlines", []) or []:
            if not isinstance(row, dict):
                continue
            headlines.append(
                MarketBriefItem(
                    title=str(row.get("title") or "Untitled"),
                    source=str(row.get("source") or "Unknown"),
                    url=str(row.get("url") or ""),
                    summary=str(row.get("summary") or ""),
                )
            )
        return MarketBriefOutput(
            generated_at=datetime.now(timezone.utc).isoformat(),
            topic=topic,
            market_overview=overview,
            headlines=headlines,
        )
