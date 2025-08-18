"""Simple web crawler using Playwright."""
from __future__ import annotations

import json
import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import Iterable, List

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from .state_manager import StateManager

class Spider:
    """Crawl websites and store raw page data."""

    def __init__(self, state: StateManager, output_file: str = "data/crawled_data.jsonl"):
        self.state = state
        self.output_path = Path(output_file)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

    def crawl(self, start_urls: Iterable[str], max_depth: int = 1) -> None:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            for url in start_urls:
                self._crawl_page(page, url, max_depth)
            browser.close()

    def _crawl_page(self, page, url: str, depth: int) -> None:
        if depth < 0 or self.state.is_visited(url):
            return
        page.goto(url)
        html = page.content()
        self._save(url, html)
        self.state.mark_visited(url)
        if depth == 0:
            return
        for link in self.extract_links(html, url):
            self._crawl_page(page, link, depth - 1)

    def extract_links(self, html: str, base_url: str) -> List[str]:
        soup = BeautifulSoup(html, "html.parser")
        links: List[str] = []
        for a in soup.find_all("a", href=True):
            links.append(urllib.parse.urljoin(base_url, a["href"]))
        return links

    def _save(self, url: str, html: str) -> None:
        record = {
            "url": url,
            "html": html,
            "timestamp": datetime.utcnow().isoformat(),
        }
        with self.output_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
