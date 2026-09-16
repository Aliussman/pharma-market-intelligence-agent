"""Tests for the market brief agent and its news sources."""

import httpx
import pytest

from src.api.main import app
from src.schemas.models import MarketBriefOutput
from src.services.market_brief import (
    ArticleSource,
    MarketBriefAgent,
    RSSSource,
    TavilySource,
)

RSS_XML = """<?xml version="1.0"?>
<rss version="2.0"><channel>
<title>Test Feed</title>
<item>
  <title>Quarterly sales rise at Pharma Co</title>
  <link>https://example.com/one</link>
  <description><![CDATA[<p>quarterly sales rose <b>8%</b></p>]]></description>
</item>
<item>
  <title>Pipeline update</title>
  <link>https://example.com/two</link>
  <description>Phase 3 trial advances</description>
</item>
</channel></rss>
"""


class FakeSource(ArticleSource):
    name = "fake"

    def __init__(self, items):
        self.items = items

    def gather(self, topic, limit):
        return self.items


class FakeLLM:
    def __init__(self, payload):
        self.payload = payload
        self.last_prompt = None

    def run_json(self, prompt):
        self.last_prompt = prompt
        return self.payload


def test_rss_source_parses_feed():
    transport = httpx.MockTransport(lambda req: httpx.Response(200, content=RSS_XML))
    with httpx.Client(transport=transport) as mock_client:
        source = RSSSource(feeds=[("Test Feed", "https://example.com/rss")], client=mock_client)
        items = source.gather(topic="pharma", limit=10)
    assert len(items) == 2
    assert items[0]["title"] == "Quarterly sales rise at Pharma Co"
    assert items[0]["source"] == "Test Feed"
    assert items[0]["snippet"] == "quarterly sales rose 8%"


def test_rss_source_skips_bad_feed():
    transport = httpx.MockTransport(lambda req: httpx.Response(500))
    with httpx.Client(transport=transport) as mock_client:
        source = RSSSource(feeds=[("Broken", "https://example.com/rss")], client=mock_client)
        items = source.gather(topic="pharma", limit=10)
    assert items == []


def test_tavily_source_maps_results():
    payload = {
        "results": [
            {
                "title": "Big Pharma earnings",
                "url": "https://reuters.com/article/1",
                "content": "Sales up",
            },
            {
                "title": "FDA decision",
                "url": "https://fiercepharma.com/news/2",
                "content": "Approval",
            },
        ]
    }
    transport = httpx.MockTransport(lambda req: httpx.Response(200, json=payload))
    with httpx.Client(transport=transport) as mock_client:
        source = TavilySource(api_key="k", client=mock_client)
        items = source.gather(topic="pharma", limit=5)
    assert len(items) == 2
    assert items[0]["source"] == "reuters.com"
    assert items[0]["snippet"] == "Sales up"


def test_agent_builds_brief_and_dedupes():
    items = [
        {"title": "A", "url": "https://x.com/1", "source": "X", "snippet": "s1"},
        {"title": "A", "url": "https://x.com/1", "source": "X", "snippet": "s1"},
        {"title": "B", "url": "https://y.com/2", "source": "Y", "snippet": "s2"},
        {"title": "", "url": "", "source": "Z", "snippet": "s3"},
    ]
    llm = FakeLLM(
        {
            "market_overview": "Market is healthy.",
            "headlines": [
                {"title": "A", "source": "X", "url": "https://x.com/1", "summary": "matters"},
                {"title": "B", "source": "Y", "url": "https://y.com/2", "summary": "also"},
            ],
        }
    )
    agent = MarketBriefAgent(llm_client=llm, sources=[FakeSource(items)])
    brief = agent.generate_brief(topic="gene therapy")

    assert isinstance(brief, MarketBriefOutput)
    assert brief.topic == "gene therapy"
    assert brief.market_overview == "Market is healthy."
    assert len(brief.headlines) == 2
    assert brief.headlines[0].url == "https://x.com/1"
    assert llm.last_prompt is not None


def test_agent_raises_when_no_articles():
    agent = MarketBriefAgent(llm_client=FakeLLM({}), sources=[FakeSource([])])
    with pytest.raises(RuntimeError):
        agent.generate_brief()


def test_market_brief_endpoint(monkeypatch):
    brief = MarketBriefOutput(
        generated_at="2026-01-01T00:00:00+00:00",
        topic="market",
        market_overview="Overview text",
        headlines=[],
    )
    monkeypatch.setattr("src.api.main.market_brief_agent.generate_brief", lambda topic: brief)

    from fastapi.testclient import TestClient

    client = TestClient(app)
    response = client.get("/market-brief", params={"topic": "gene therapy"})
    assert response.status_code == 200
    body = response.json()
    assert body["topic"] == "market"
    assert body["market_overview"] == "Overview text"
