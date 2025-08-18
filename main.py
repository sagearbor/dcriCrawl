"""Main runner to orchestrate crawling, analysis, and aggregation."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List

from src.crawler.spider import Spider
from src.crawler.state_manager import StateManager
from src.analyzer.pipeline import analyze_crawled_data
from src.aggregator.aggregator import aggregate_and_save


def load_settings(path: str = "config/settings.yaml") -> Dict[str, str]:
    """Load simple key-value settings from a YAML file.

    This lightweight parser handles the minimal configuration used in the
    project without requiring external dependencies.
    """
    settings: Dict[str, str] = {}
    config_path = Path(path)
    if not config_path.exists():
        return settings
    with config_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or ":" not in line:
                continue
            key, value = line.split(":", 1)
            settings[key.strip()] = value.strip().strip("'\"")
    return settings


def read_urls(path: str) -> List[str]:
    """Read newline-delimited URLs from ``path``."""
    url_path = Path(path)
    if not url_path.exists():
        return []
    with url_path.open("r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def run_crawl(settings: Dict[str, str]) -> None:
    """Execute the crawling stage."""
    urls = read_urls(settings.get("urls_file", "data/urls_to_crawl.txt"))
    if not urls:
        return
    state = StateManager()
    spider = Spider(
        state,
        output_file=settings.get("output_file", "data/crawled_data.jsonl"),
    )
    max_depth = int(settings.get("max_depth", 1))
    spider.crawl(urls, max_depth=max_depth)


def run_analysis(settings: Dict[str, str]) -> None:
    """Execute the analysis stage."""
    input_file = settings.get("output_file", "data/crawled_data.jsonl")
    analyze_crawled_data(input_file, "data/analysis_results.jsonl")


def run_aggregation() -> None:
    """Execute the aggregation stage."""
    aggregate_and_save("data/analysis_results.jsonl", "data/domain_summary.csv")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run crawler pipeline")
    parser.add_argument(
        "--crawl", action="store_true", help="Run the crawling stage"
    )
    parser.add_argument(
        "--analyze", action="store_true", help="Run the analysis stage"
    )
    parser.add_argument(
        "--aggregate", action="store_true", help="Run the aggregation stage"
    )
    args = parser.parse_args()

    settings = load_settings()

    if not any([args.crawl, args.analyze, args.aggregate]):
        args.crawl = args.analyze = args.aggregate = True

    if args.crawl:
        run_crawl(settings)
    if args.analyze:
        run_analysis(settings)
    if args.aggregate:
        run_aggregation()


if __name__ == "__main__":
    main()
