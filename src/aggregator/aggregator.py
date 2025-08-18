"""Aggregate page-level analysis results by domain."""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Dict, Any
from urllib.parse import urlparse


def aggregate_by_domain(
    input_file: str = "data/analysis_results.jsonl",
    min_pages: int = 1,
) -> Dict[str, Dict[str, Any]]:
    """Aggregate analysis results by root domain.

    Args:
        input_file: Path to the JSONL file containing page-level analysis.
        min_pages: Minimum number of pages required for a domain to be included.

    Returns:
        Mapping of domain to summary statistics including page count and unique keywords.
    """
    path = Path(input_file)
    aggregated: Dict[str, Dict[str, Any]] = {}

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            url = record.get("url", "")
            domain = urlparse(url).netloc
            if not domain:
                continue
            summary = aggregated.setdefault(
                domain,
                {"pages": 0, "ai_keywords": set(), "policy_keywords": set()},
            )
            summary["pages"] += 1
            keywords = record.get("keywords", {})
            summary["ai_keywords"].update(keywords.get("ai", []))
            summary["policy_keywords"].update(keywords.get("policy", []))

    # convert sets to sorted lists for deterministic output
    for summary in aggregated.values():
        summary["ai_keywords"] = sorted(summary["ai_keywords"])
        summary["policy_keywords"] = sorted(summary["policy_keywords"])

    # filter out domains with too few pages
    aggregated = {
        domain: data
        for domain, data in aggregated.items()
        if data["pages"] >= min_pages
    }

    return aggregated


def save_aggregated_csv(
    aggregated: Dict[str, Dict[str, Any]],
    output_file: str = "data/domain_summary.csv",
) -> None:
    """Save aggregated domain data to a CSV file."""
    path = Path(output_file)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(
            csvfile, fieldnames=["domain", "pages", "ai_keywords", "policy_keywords"]
        )
        writer.writeheader()
        for domain, data in aggregated.items():
            writer.writerow(
                {
                    "domain": domain,
                    "pages": data["pages"],
                    "ai_keywords": ",".join(data["ai_keywords"]),
                    "policy_keywords": ",".join(data["policy_keywords"]),
                }
            )


def aggregate_and_save(
    input_file: str = "data/analysis_results.jsonl",
    output_file: str = "data/domain_summary.csv",
    min_pages: int = 1,
) -> Dict[str, Dict[str, Any]]:
    """Convenience function to aggregate analysis results and save to CSV."""
    aggregated = aggregate_by_domain(input_file, min_pages=min_pages)
    save_aggregated_csv(aggregated, output_file)
    return aggregated


if __name__ == "__main__":  # pragma: no cover - manual execution
    aggregate_and_save()
