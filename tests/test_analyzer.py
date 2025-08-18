import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.analyzer import detect_keywords


def test_detect_keywords_finds_ai_and_policy_terms():
    text = "Our organization uses Artificial Intelligence (AI) to process data. See our privacy policy for details."
    result = detect_keywords(text)
    assert "artificial intelligence" in result["ai"]
    assert "ai" in result["ai"]
    assert "privacy" in result["policy"]
    assert "policy" in result["policy"]


def test_detect_keywords_returns_empty_lists_when_no_matches():
    text = "This sentence has none of the monitored words."
    result = detect_keywords(text)
    assert result["ai"] == []
    assert result["policy"] == []
