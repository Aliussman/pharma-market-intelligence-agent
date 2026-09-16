"""Tests for prompt selection."""

import pytest

from src.llm.prompts import (
    PHARMA_PROMPT_TEMPLATE,
    finance_prompt,
    pharma_prompt,
    select_prompt,
)

REQUIRED_KEYS = [
    "financial_summary",
    "priority_brands",
    "pipeline_regulatory",
    "strategic_insights",
]


def test_pharma_prompt_contains_output_format():
    prompt = pharma_prompt("Company X announced a new vaccine.")
    for key in REQUIRED_KEYS:
        assert key in prompt
    assert "Company X announced a new vaccine." in prompt


def test_finance_prompt_contains_output_format():
    prompt = finance_prompt("Revenue grew 8% last quarter.")
    for key in REQUIRED_KEYS:
        assert key in prompt
    assert "Revenue grew 8% last quarter." in prompt


@pytest.mark.parametrize(
    "text",
    [
        "Quarterly sales rose to $4.2B with EPS of $1.10",
        "net sales and operating income improved",
        "strong cash flow and margin expansion",
    ],
)
def test_select_prompt_picks_finance(text):
    assert select_prompt(text) == finance_prompt(text)


@pytest.mark.parametrize(
    "text",
    [
        "The company advanced its Phase 3 oncology trial",
        "regulatory approval for the gene therapy",
    ],
)
def test_select_prompt_picks_pharma(text):
    assert select_prompt(text) == pharma_prompt(text)


def test_templates_must_be_formatted_with_keys():
    with pytest.raises(KeyError):
        PHARMA_PROMPT_TEMPLATE.format(output_format="x")
