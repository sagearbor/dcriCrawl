"""Pipeline to analyze crawled HTML data for keywords."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any

from bs4 import BeautifulSoup

from .keyword_detector import detect_keywords


def _extract_text(html: str) -> str:
    """Extract visible text from HTML using BeautifulSoup."""
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(" ", strip=True)


def analyze_crawled_data(
    input_file: str = "data/crawled_data.jsonl",
    output_file: str = "data/analysis_results.jsonl",
) -> None:
    """Read crawled data and write keyword analysis results.

    Args:
        input_file: Path to the JSONL file produced by the crawler.
        output_file: Path to the JSONL file where analysis results will be stored.
    """
    in_path = Path(input_file)
    out_path = Path(output_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with in_path.open("r", encoding="utf-8") as f_in, out_path.open(
        "w", encoding="utf-8"
    ) as f_out:
        for line in f_in:
            record: Dict[str, Any] = json.loads(line)
            text = _extract_text(record.get("html", ""))
            keywords = detect_keywords(text)
            result = {
                "url": record.get("url"),
                "timestamp": record.get("timestamp"),
                "keywords": keywords,
            }
            f_out.write(json.dumps(result) + "\n")


if __name__ == "__main__":  # pragma: no cover - manual execution
    analyze_crawled_data()
