import json
from pathlib import Path
from unittest.mock import MagicMock

from src.crawler.spider import Spider
from src.crawler.state_manager import StateManager


def test_extract_links():
    html = '<a href="/a">A</a><a href="https://example.com/b">B</a>'
    state = StateManager(state_file="/tmp/state.json")
    spider = Spider(state, output_file="/tmp/out.jsonl")
    links = spider.extract_links(html, "https://example.com")
    assert set(links) == {"https://example.com/a", "https://example.com/b"}


def test_save_and_state(tmp_path):
    state_file = tmp_path / "state.json"
    out_file = tmp_path / "out.jsonl"
    state = StateManager(state_file=str(state_file))
    spider = Spider(state, output_file=str(out_file))

    page = MagicMock()
    page.content.return_value = "<html></html>"
    page.goto.return_value = None

    spider._crawl_page(page, "https://example.com", depth=0)

    assert state.is_visited("https://example.com")
    data = [json.loads(line) for line in out_file.read_text().splitlines()]
    assert data[0]["url"] == "https://example.com"
