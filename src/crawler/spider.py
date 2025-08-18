"""Simple web crawler using Playwright."""
from __future__ import annotations

import json
import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Optional

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from .state_manager import StateManager


class Spider:
    """Crawl websites and store raw page data."""

    def __init__(
        self,
        state: StateManager,
        output_file: str = "data/crawled_data.jsonl",
        auth_state: Optional[str] = None,
    ) -> None:
        self.state = state
        self.output_path = Path(output_file)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.auth_state = auth_state

    def crawl(self, start_urls: Iterable[str], max_depth: int = 1) -> None:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context_args = {}
            if self.auth_state and Path(self.auth_state).exists():
                context_args["storage_state"] = self.auth_state
            context = browser.new_context(**context_args)
            page = context.new_page()
            for url in start_urls:
                self.state.record_discovered(url)
                self._crawl_page(page, url, max_depth)
            browser.close()

    def _crawl_page(self, page, url: str, depth: int) -> None:
        if depth < 0:
            return
        page.goto(url)
        html = page.content()
        if self.state.is_visited(url) and not self.state.has_changed(url, html):
            return
        self._save(url, html)
        self.state.mark_visited(url, html)
        links = self.extract_links(html, url)
        for link in links:
            self.state.record_discovered(link)
            if depth > 0:
                self._crawl_page(page, link, depth - 1)

    def extract_links(self, html: str, base_url: str) -> List[str]:
        soup = BeautifulSoup(html, "html.parser")
        links: List[str] = []
        seen = set()
        for a in soup.find_all("a", href=True):
            raw_href = a["href"]
            if raw_href.startswith("#"):
                continue
            href = urllib.parse.urljoin(base_url, raw_href)
            parsed = urllib.parse.urlparse(href)
            if parsed.scheme not in {"http", "https"}:
                continue
            if href in seen:
                continue
            seen.add(href)
            links.append(href)
        return links

    def _save(self, url: str, html: str) -> None:
        record = {
            "url": url,
            "html": html,
            "timestamp": datetime.utcnow().isoformat(),
        }
        with self.output_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
